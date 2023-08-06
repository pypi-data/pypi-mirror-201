""" Run Input """
from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Sequence

import yaml
from typing_extensions import TypedDict

from mcli.api.exceptions import MAPIException, MCLIRunConfigValidationError
from mcli.api.schema.generic_model import DeserializableModel
from mcli.models.mcli_cluster import Cluster
from mcli.utils.utils_config import (BaseSubmissionConfig, EnvVarTranslation, IntegrationTranslation, Translation,
                                     uuid_generator)
from mcli.utils.utils_string_functions import (MAX_KUBERNETES_LENGTH, ensure_rfc1123_compatibility, validate_image,
                                               validate_rfc1123_name)

logger = logging.getLogger(__name__)
RUN_CONFIG_UID_LENGTH = 6
VALID_OPTIMIZATION_LEVELS = frozenset([0, 1, 2, 3])
MAX_RUN_NAME_LENGTH = MAX_KUBERNETES_LENGTH - RUN_CONFIG_UID_LENGTH - 1  # -1 for the dash


class SchedulingConfig(TypedDict):
    """Typed dictionary for nested scheduling configurations"""
    priority: Optional[str]


class ComputeConfig(TypedDict):
    """Typed dictionary for nested compute requests"""
    cluster: Optional[str]
    instance: Optional[str]
    nodes: Optional[int]
    gpu_type: Optional[str]
    gpus: Optional[int]
    cpus: Optional[int]


def strip_nones(d: Dict[str, Any]) -> Dict[str, Any]:
    """Remove all keys with None values from a dictionary"""
    return {k: v for k, v in d.items() if v is not None}


@dataclass
class FinalRunConfig(DeserializableModel):
    """A finalized run configuration

    This configuration must be complete, with enough details to submit a new run to the
    MosaicML platform.
    """

    run_id: str
    name: str
    cpus: int
    image: str
    integrations: List[Dict[str, Any]]
    env_variables: List[Dict[str, str]]

    parameters: Dict[str, Any]

    gpu_type: Optional[str] = None  # deprecating in favor of compute['gpu_type']
    gpu_num: Optional[int] = None  # deprecating in favor of compute['gpus']

    optimization_level: int = 0
    # Make both optional for initial rollout
    # Eventually make entrypoint required and deprecate command
    command: str = ''
    entrypoint: str = ''

    # Platform is deprecated, but not required for backwards compatibility
    cluster: str = ''
    platform: str = ''

    # Partition is an optional new keyword
    partitions: Optional[List[str]] = None

    # Scheduling parameters - optional for backwards-compatibility
    # pylint: disable-next=unnecessary-lambda
    scheduling: SchedulingConfig = field(default_factory=lambda: SchedulingConfig(**{}))

    # Compute parameters - optional for backwards-compatibility
    # pylint: disable-next=unnecessary-lambda
    compute: ComputeConfig = field(default_factory=lambda: ComputeConfig(**{}))

    _property_translations = {
        'run_id': 'run_id',
        'runName': 'name',
        'gpuType': 'gpu_type',
        'gpuNum': 'gpu_num',
        'cpus': 'cpus',
        'cluster': 'cluster',
        'image': 'image',
        'optimizationLevel': 'optimization_level',
        'integrations': 'integrations',
        'envVariables': 'env_variables',
        'parameters': 'parameters',
        'command': 'command',
        'entrypoint': 'entrypoint',
        'scheduling': 'scheduling',
        'compute': 'compute',
    }

    _optional_properties = {
        'partitions',
        'scheduling',
        'compute',
    }

    def __str__(self) -> str:
        return yaml.safe_dump(asdict(self))

    def __post_init__(self):
        self.cluster = self.cluster or self.platform

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> FinalRunConfig:
        missing = set(cls._property_translations) - set(response) - cls._optional_properties
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=
                f'Missing required key(s) in response to deserialize FinalRunConfig object: {", ".join(missing)}',
            )
        data = {}
        for k, v in cls._property_translations.items():
            if k not in response:
                # This must be an optional property, so skip
                continue
            value = response[k]
            if v == 'env_variables':
                value = EnvVarTranslation.from_mapi(value)
            elif v == 'integrations':
                value = IntegrationTranslation.from_mapi(value)
            elif v == 'scheduling':
                value = SchedulingTranslation.from_mapi(value)
            elif v == 'compute':
                value = ComputeTranslation.from_mapi(value)
            data[v] = value

        return cls(**data)

    @classmethod
    def finalize_config(cls, run_config: RunConfig) -> FinalRunConfig:  # pylint: disable=too-many-statements
        """Create a :class:`~mcli.models.run_config.FinalRunConfig` from the provided
        :class:`~mcli.models.run_config.RunConfig`.

        If the :class:`~mcli.models.run_config.RunConfig` is not fully populated then
        this function fails with an error.

        Args:
            run_config (:class:`~mcli.models.run_config.RunConfig`): The RunConfig to finalize

        Returns:
            :class:`~mcli.models.run_config.FinalRunConfig`: The object created using values from the input

        Raises:
            :class:`~mcli.api.exceptions.MCLIConfigError`: If MCLI config is not present or is missing information
            :class:`~mcli.api.exceptions.MCLIRunConfigValidationError`: If run_config is not valid
        """
        # pylint: disable-next=import-outside-toplevel
        from mcli.config import MCLIConfig
        conf = MCLIConfig.load_config(safe=True)

        if run_config.cpus is None:
            run_config.cpus = 0

        # MosaicML Agent is disabled for all external users
        if not conf.internal or run_config.optimization_level is None:
            # TODO: not all docker images will support adding the MosaicML Agent
            # If you change the default optimization level for all users, make
            # sure the hello world documentation (image: bash) still works
            run_config.optimization_level = 0

        if run_config.partitions is not None:
            # Validate provided partition is a list of strings
            if not isinstance(run_config.partitions, Sequence):
                run_config.partitions = [str(run_config.partitions)]
            else:
                run_config.partitions = [str(p) for p in run_config.partitions]

        model_as_dict = asdict(run_config)

        # Remove deprecated run_name
        model_as_dict.pop('run_name', None)

        # Remove deprecated platform
        model_as_dict.pop('platform', None)
        model_as_dict = strip_nones(model_as_dict)

        # Fill in default initial values for FinalRunConfig
        model_as_dict.update({
            'run_id': uuid_generator(RUN_CONFIG_UID_LENGTH),
        })

        model_as_dict['name'] = _clean_run_name(model_as_dict.get('name'))

        if isinstance(model_as_dict.get('gpu_type'), int):
            model_as_dict['gpu_type'] = str(model_as_dict['gpu_type'])

        # Convert and validate optimization level
        try:
            model_as_dict['optimization_level'] = int(model_as_dict['optimization_level'])
            if model_as_dict['optimization_level'] not in VALID_OPTIMIZATION_LEVELS:
                raise ValueError
        except ValueError as e:
            raise MCLIRunConfigValidationError(
                f'"{model_as_dict["optimization_level"]}" is not a valid optimization level. '
                f'Please choose from: {", ".join(str(i) for i in VALID_OPTIMIZATION_LEVELS)}') from e

        image = model_as_dict.get('image')
        if not image:
            raise MCLIRunConfigValidationError('An image name must be provided using the keyword [bold]image[/]')
        elif not validate_image(image):
            raise MCLIRunConfigValidationError(f'The image name "{model_as_dict["image"]}" is not valid')

        # Do not support specifying both a command and an entrypoint because the two might
        # conflict with each other
        if run_config.command and run_config.entrypoint:
            raise MCLIRunConfigValidationError(
                'Specifying both [bold]command[/] and [bold]entrypoint[/] as input is not supported.'
                'Please only specify only one.')

        if not (run_config.command or run_config.entrypoint):
            raise MCLIRunConfigValidationError('A command to run must be provided using the keyword [bold]command[/]')

        return cls(**model_as_dict)

    def to_create_run_api_input(self) -> Dict[str, Dict[str, Any]]:
        """Convert a run configuration to a proper JSON to pass to MAPI's createRun

        Returns:
            Dict[str, Dict[str, Any]]: The run configuration as a MAPI runInput JSON
        """
        translations = {v: k for k, v in self._property_translations.items()}

        translated_input = {}
        for field_name, value in asdict(self).items():
            if value is None:
                continue
            translated_name = translations.get(field_name, field_name)
            if field_name == 'env_variables':
                value = EnvVarTranslation.to_mapi(value)
            elif field_name == 'integrations':
                value = IntegrationTranslation.to_mapi(value)
            elif field_name == "scheduling":
                value = SchedulingTranslation.to_mapi(value)
            elif field_name == "compute":
                value = ComputeTranslation.to_mapi(value)
            elif field_name == "gpu_type" and not value:
                continue
            elif field_name == "cluster" and not value:
                continue
            elif field_name == "platform":
                continue
            elif isinstance(value, dict):
                value = strip_nones(value)

            translated_input[translated_name] = value
        return {
            'runInput': translated_input,
        }


class SchedulingTranslation(Translation[SchedulingConfig, Dict[str, Any]]):
    """Translate scheduling configs to and from MAPI"""

    @classmethod
    def from_mapi(cls, value: Dict[str, Any]) -> SchedulingConfig:
        extracted: SchedulingConfig = {'priority': None}
        for k, v in value.items():
            if k == 'priority':
                extracted['priority'] = v
        return extracted

    @classmethod
    def to_mapi(cls, value: SchedulingConfig) -> Dict[str, Any]:
        processed: Dict[str, Any] = {}
        for k, v in value.items():
            if v is not None:
                processed[k] = v
        return processed


class ComputeTranslation(Translation[ComputeConfig, Dict[str, Any]]):
    """Translate compute configs to and from MAPI"""

    translations = {
        "gpuType": "gpu_type",
    }

    @classmethod
    def from_mapi(cls, value: Dict[str, Any]) -> ComputeConfig:
        extracted = ComputeConfig(**{cls.translations.get(k, k): v for k, v in value.items()})
        return extracted

    @classmethod
    def to_mapi(cls, value: ComputeConfig) -> Dict[str, Any]:
        inv = {v: k for k, v in cls.translations.items()}
        processed = {inv.get(k, k): v for k, v in value.items() if v is not None}
        return processed


def _clean_run_name(run_name: Optional[str]) -> str:
    if run_name is None:
        raise MCLIRunConfigValidationError('A run name must be provided using the keyword [bold]name[/]')

    name_validation = validate_rfc1123_name(text=run_name)
    if name_validation.valid:
        return run_name

    # TODO: Remove this once all users are on MCloud and rely on MCloud to do this validation
    if len(run_name) > MAX_RUN_NAME_LENGTH:
        raise MCLIRunConfigValidationError(f'Run name cannot be more than {MAX_RUN_NAME_LENGTH} characters.')

    # TODO: Figure out why logging strips out regex []
    # (This is a rich formatting thing. [] is used to style text)
    new_run_name = ensure_rfc1123_compatibility(run_name)

    logger.warning(f'Invalid run name "{run_name}": Run names must be less than {MAX_RUN_NAME_LENGTH} '
                   'characters and contain only lower-case letters, numbers, or "-". '
                   f'Converting to a valid name: {new_run_name}')
    return new_run_name


def _validate_cluster_exists(cluster: str):
    """Validate that the cluster exists, if not throw a MCLIValidationError
    """
    try:
        _ = Cluster.get_by_name(cluster)
    except KeyError as e:
        # pylint: disable-next=import-outside-toplevel
        from mcli.config import FeatureFlag, MCLIConfig

        conf = MCLIConfig.load_config(True)
        if not conf.feature_enabled(FeatureFlag.USE_MCLOUD):
            cluster_names = ', '.join([c.name for c in conf.clusters])
            if cluster_names:
                raise MCLIRunConfigValidationError(
                    f'Invalid cluster requested: {cluster}. '
                    'If you think this should be a valid cluster, try creating the cluster '
                    f'first with:\n\nmcli create cluster {cluster}\n\n'
                    f'Otherwise, choose one of: {cluster_names}') from e
            else:
                raise MCLIRunConfigValidationError(
                    f'Invalid cluster requested: {cluster}. '
                    'User has not created any clusters. '
                    'If you think this should be a valid cluster, try creating the cluster '
                    f'first with:\n\nmcli create cluster {cluster}') from e
        raise


@dataclass
class RunConfig(BaseSubmissionConfig):
    """A run configuration for the MosaicML platform

    Values in here are not yet validated and some required values may be missing.

    Args:
        name (`Optional[str]`): User-defined name of the run
        gpu_type (`Optional[str]`): GPU type (optional if only one gpu type for your cluster)
        gpu_num (`Optional[int]`): Number of GPUs
        cpus (`Optional[int]`): Number of CPUs
        cluster (`Optional[str]`): Cluster to use (optional if you only have one)
        image (`Optional[str]`): Docker image (e.g. `mosaicml/composer`)
        integrations (`List[Dict[str, Any]]`): List of integrations
        env_variables (`List[Dict[str, str]]`): List of environment variables
        command (`str`): Command to use when a run starts
        parameters (`Dict[str, Any]`): Parameters to mount into the environment
        entrypoint (`str`): Alternative to command
    """
    run_name: Optional[str] = None
    name: Optional[str] = None
    gpu_type: Optional[str] = None
    gpu_num: Optional[int] = None
    cpus: Optional[int] = None
    platform: Optional[str] = None
    cluster: Optional[str] = None
    image: Optional[str] = None
    partitions: Optional[List[str]] = None
    optimization_level: Optional[int] = None
    integrations: List[Dict[str, Any]] = field(default_factory=list)
    env_variables: List[Dict[str, str]] = field(default_factory=list)
    # pylint: disable-next=unnecessary-lambda
    scheduling: SchedulingConfig = field(default_factory=lambda: SchedulingConfig(**{}))
    # pylint: disable-next=unnecessary-lambda
    compute: ComputeConfig = field(default_factory=lambda: ComputeConfig(**{}))

    command: str = ''
    parameters: Dict[str, Any] = field(default_factory=dict)
    entrypoint: str = ''

    _property_translations = {
        'runName': 'name',
        'gpuNum': 'gpu_num',
        'cpus': 'cpus',
        'cluster': 'cluster',
        'image': 'image',
        'optimizationLevel': 'optimization_level',
        'integrations': 'integrations',
        'envVariables': 'env_variables',
        'parameters': 'parameters',
        'command': 'command',
        'entrypoint': 'entrypoint',
        'scheduling': 'scheduling',
    }

    _optional_display_properties = {
        'cpus', 'env_variables', 'entrypoint', 'gpu_type', 'integrations', 'optimization_level', 'parameters',
        'partitions', 'platform', 'run_name', 'scheduling'
    }

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> RunConfig:
        data = {}
        for k, v in cls._property_translations.items():
            if k not in response:
                # This must be an optional property, so skip
                continue
            value = response[k]
            if v == 'env_variables':
                value = EnvVarTranslation.from_mapi(value)
            elif v == 'integrations':
                value = IntegrationTranslation.from_mapi(value)
            elif v == 'scheduling':
                value = SchedulingTranslation.from_mapi(value)
            elif v == 'compute':
                value = ComputeConfig(**value)
            data[v] = value

        return cls(**data)

    def __post_init__(self):
        self.name = self.name or self.run_name
        if self.run_name is not None:
            logger.debug('Field "run_name" is deprecated. Please use "name" instead')

        self.cluster = self.cluster or self.platform
        if self.platform is not None:
            logger.debug('Field "platform" is deprecated. Please use "cluster" instead')
