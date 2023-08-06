""" Functions for deleting MCLI objects """
import fnmatch
import logging
from http import HTTPStatus
from typing import Dict, Generic, List, Optional, TypeVar

from mcli.api.exceptions import KubernetesException, MAPIException, cli_error_handler
from mcli.api.secrets import delete_secrets as api_delete_secrets
from mcli.api.secrets import get_secrets as api_get_secrets
from mcli.cli.common.deployment_filters import get_deployments_with_filters
from mcli.cli.common.run_filters import get_runs_with_filters
from mcli.config import MESSAGE, FeatureFlag, MCLIConfig, MCLIConfigError
from mcli.models import Cluster
from mcli.objects.secrets.cluster_secret import SecretManager
from mcli.sdk import InferenceDeployment, Run, delete_inference_deployments, delete_runs
from mcli.utils.utils_interactive import query_yes_no
from mcli.utils.utils_logging import FAIL, INFO, OK, WARN, get_indented_list
from mcli.utils.utils_run_status import RunStatus
from mcli.utils.utils_spinner import console_status

logger = logging.getLogger(__name__)

# pylint: disable-next=invalid-name
T_NOUN = TypeVar('T_NOUN')


class DeleteGroup(Generic[T_NOUN]):
    """Helper for extracting objects to delete from an existing set
    """

    def __init__(self, requested: List[str], existing: Dict[str, T_NOUN]):
        # Get unique values, with order
        self.requested = list(dict.fromkeys(requested))
        self.existing = existing

        self.chosen: Dict[str, T_NOUN] = {}
        self.missing: List[str] = []
        for pattern in self.requested:
            matching = fnmatch.filter(self.existing, pattern)
            if matching:
                self.chosen.update({k: self.existing[k] for k in matching})
            else:
                self.missing.append(pattern)

        self.remaining = {k: v for k, v in self.existing.items() if k not in self.chosen}


def delete_environment_variable(variable_names: List[str],
                                force: bool = False,
                                delete_all: bool = False,
                                **kwargs) -> int:
    del kwargs
    if not (variable_names or delete_all):
        logger.error(f'{FAIL} Must specify environment variable names or --all.')
        return 1
    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if delete_all:
        variable_names = ['*']

    group = DeleteGroup(variable_names, {ev.key: ev for ev in conf.environment_variables})

    # Some environment variables couldn't be found. Throw a warning and continue
    if group.missing:
        if group.remaining:
            suggestion = f'Maybe you meant one of: {", ".join(sorted(list(group.remaining)))}?'
        else:
            suggestion = 'No environment variables exist.'

        logger.warning(
            f'{INFO} Could not find environment variable(s) matching: {", ".join(sorted(group.missing))}. {suggestion}')

    # Nothing to delete, so error
    if not group.chosen:
        logger.error(f'{FAIL} No environment variables to delete')
        return 1

    if not force:
        if len(group.chosen) > 1:
            logger.info(f'{INFO} Ready to delete environment variables:\n'
                        f'{get_indented_list(sorted(list(group.chosen)))}\n')
            confirm = query_yes_no('Would you like to delete the environment variables listed above?')
        else:
            chosen_ev = list(group.chosen)[0]
            confirm = query_yes_no(f'Would you like to delete the environment variable: {chosen_ev}?')
        if not confirm:
            logger.error('Canceling deletion')
            return 1

    conf.environment_variables = list(group.remaining.values())
    conf.save_config()
    return 0


def _confirm_secret_deletion(secrets):
    if len(secrets) > 1:
        logger.info(f'{INFO} Ready to delete secrets:\n'
                    f'{get_indented_list(sorted(secrets))}\n')
        details = ' listed above'
    else:
        details = f': {list(secrets)[0]}'
    confirm = query_yes_no(f'Would you like to delete the secret{details}?')

    if not confirm:
        raise RuntimeError('Canceling deletion')


def delete_secret(secret_names: List[str], force: bool = False, delete_all: bool = False, **kwargs) -> int:
    """Delete the requested secret(s) from the user's clusters

    Args:
        secret_names: List of secrets to delete
        force: If True, do not request confirmation. Defaults to False.

    Returns:
        True if deletion was successful
    """
    del kwargs

    if not (secret_names or delete_all):
        logger.error(f'{FAIL} Must specify secret names or --all.')
        return 1

    try:
        conf: MCLIConfig = MCLIConfig.load_config(safe=True)
        if conf.feature_enabled(FeatureFlag.USE_MCLOUD):
            # Get secrets to delete
            to_delete_secrets = api_get_secrets(secret_names) if not delete_all else api_get_secrets()
            if not to_delete_secrets:
                if secret_names:
                    logger.warning(f'{INFO} Could not find secrets(s) matching: {", ".join(secret_names)}')
                else:
                    logger.warning(f'{INFO} Could not find any secrets')
                return 1

            # Confirm and delete
            if not force:
                _confirm_secret_deletion(to_delete_secrets)
            with console_status('Deleting secrets..'):
                deleted = api_delete_secrets(secrets=to_delete_secrets, timeout=None)
            logger.info(f'{OK} Deleted secret(s): {", ".join([s.name for s in deleted])}')
        else:
            if delete_all:
                secret_names = ['*']

            kube_delete_secret(secret_names, conf, force)

    except (KubernetesException, MAPIException) as e:
        if e.status == HTTPStatus.NOT_FOUND:
            logger.error(f'{FAIL} No secrets to delete')
        else:
            logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    return 0


def kube_delete_secret(secret_names: List[str], conf: MCLIConfig, force: bool = False):

    if not conf.clusters:
        raise KubernetesException(
            HTTPStatus.NOT_FOUND,
            'No clusters found. You must have at least 1 cluster added before working with secrets.')

    # Note, we could just attempt to delete and catch the error.
    # I think it's a bit cleaner to first check if the secret exists, but this will be a bit slower
    # This slowness should be OK for secrets since they are generally small in number

    ref_cluster = conf.clusters[0]
    secret_manager = SecretManager(ref_cluster)

    group = DeleteGroup(secret_names, {ps.secret.name: ps for ps in secret_manager.get_secrets()})

    # Some clusters couldn't be found. Throw a warning and continue
    if group.missing:
        if group.remaining:
            suggestion = f'Maybe you meant one of: {", ".join(sorted(list(group.remaining)))}?'
        else:
            suggestion = 'No secrets exist.'

        logger.warning(f'{INFO} Could not find secrets(s) matching: {", ".join(sorted(group.missing))}. {suggestion}')

    if not group.chosen:
        raise KubernetesException(HTTPStatus.NOT_FOUND, 'No secrets to delete')

    if not force:
        _confirm_secret_deletion(group.chosen)

    failures: Dict[str, List[str]] = {}
    with console_status('Deleting secrets...') as status:
        for cluster in conf.clusters:
            with Cluster.use(cluster):
                status.update(f'Deleting secrets from {cluster.name}...')
                for ps in group.chosen.values():
                    success = ps.delete(cluster.namespace)
                    if not success:
                        failures.setdefault(ps.secret.name, []).append(cluster.name)

    deleted = sorted([name for name in group.chosen if name not in failures])
    if deleted:
        logger.info(f'{OK} Deleted secret(s): {", ".join(deleted)}')

    if failures:
        for name, failed_clusters in failures.items():
            logger.error(f'Secret {name} could not be deleted from platform(s): {", ".join(sorted(failed_clusters))}')
        raise KubernetesException(HTTPStatus.INTERNAL_SERVER_ERROR,
                                  f'Could not delete secret(s): {", ".join(sorted(list(failures.keys())))}')


def delete_cluster(cluster_names: List[str], force: bool = False, delete_all: bool = False, **kwargs) -> int:
    del kwargs

    if not (cluster_names or delete_all):
        logger.error(f'{FAIL} Must specify cluster names or --all.')
        return 1

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if delete_all:
        cluster_names = ['*']

    group = DeleteGroup(cluster_names, {pl.name: pl for pl in conf.clusters})

    # Some clusters couldn't be found. Throw a warning and continue
    if group.missing:
        if group.remaining:
            suggestion = f'Maybe you meant one of: {", ".join(sorted(list(group.remaining)))}?'
        else:
            suggestion = 'No clusters exist.'
        logger.warning(f'{INFO} Could not find cluster(s) matching: {", ".join(sorted(group.missing))}. {suggestion}')

    # Nothing to delete, so error
    if not group.chosen:
        logger.error(f'{FAIL} No cluster to delete')
        return 1

    if not force:
        if len(group.chosen) > 1:
            logger.info(f'{INFO} Ready to delete clusters:\n'
                        f'{get_indented_list(sorted(list(group.chosen)))}\n')
            confirm = query_yes_no('Would you like to delete the clusters listed above?')
        else:
            chosen_cluster = list(group.chosen)[0]
            confirm = query_yes_no(f'Would you like to delete the cluster: {chosen_cluster}?')
        if not confirm:
            logger.error(f'{FAIL} Canceling deletion')
            return 1

    conf.clusters = list(group.remaining.values())
    conf.save_config()

    logger.info(f"{OK} Deleted cluster{'s' if len(group.chosen) > 1 else ''}: {', '.join(list(group.chosen.keys()))}")
    return 0


def confirm_run_update(runs: List[Run], action: str = 'delete') -> int:
    num_runs_compressed_view = 50

    if len(runs) == 1:
        chosen_run = list(runs)[0].name
        return query_yes_no(f'Would you like to {action} the run: {chosen_run}?')
    elif len(runs) < num_runs_compressed_view:
        pretty_runs = get_indented_list(sorted(r.name for r in runs))
        logger.info(f'{INFO} Ready to {action} runs:\n{pretty_runs}\n')
        return query_yes_no(f'Would you like to {action} the runs listed above?')

    logger.info(f'Ready to {action} {len(runs)} runs')
    return query_yes_no(f'Would you like to {action} all {len(runs)} runs?')


@cli_error_handler('mcli delete run')
def delete_run(
    name_filter: Optional[List[str]] = None,
    cluster_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    gpu_type_filter: Optional[List[str]] = None,
    gpu_num_filter: Optional[List[int]] = None,
    status_filter: Optional[List[RunStatus]] = None,
    latest: bool = False,
    delete_all: bool = False,
    force: bool = False,
    **kwargs,
):
    del kwargs

    runs = get_runs_with_filters(
        name_filter,
        cluster_filter,
        before_filter,
        after_filter,
        gpu_type_filter,
        gpu_num_filter,
        status_filter,
        latest,
        delete_all,
    )

    if not runs:
        extra = '' if delete_all else ' matching the specified criteria'
        logger.error(f'{WARN} No runs found{extra}.')
        return 1

    if not force and not confirm_run_update(runs, 'delete'):
        logger.error(f'{FAIL} Canceling delete runs')
        return 1

    with console_status('Deleting runs...'):
        delete_runs(runs)

    logger.info(f'{OK} Deleted runs')
    return 0


def confirm_deployment_update(deployments: List[InferenceDeployment], action: str = 'delete') -> int:
    num_deployments_compressed_view = 50

    if len(deployments) == 1:
        chosen_run = list(deployments)[0].name
        return query_yes_no(f'Would you like to {action} the deployment: {chosen_run}?')
    elif len(deployments) < num_deployments_compressed_view:
        pretty_deployments = get_indented_list(sorted(d.name for d in deployments))
        logger.info(f'{INFO} Ready to {action} deployments:\n{pretty_deployments}\n')
        return query_yes_no(f'Would you like to {action} the deployments listed above?')

    return query_yes_no(f'Would you like to {action} all {len(deployments)} deployments?')


@cli_error_handler('mcli delete deployment')
def delete_deployment(
    name_filter: Optional[List[str]] = None,
    cluster_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    gpu_type_filter: Optional[List[str]] = None,
    gpu_num_filter: Optional[List[int]] = None,
    status_filter: Optional[List[str]] = None,
    latest: bool = False,
    delete_all: bool = False,
    force: bool = False,
    **kwargs,
):
    del kwargs

    deployments = get_deployments_with_filters(
        name_filter,
        cluster_filter,
        before_filter,
        after_filter,
        gpu_type_filter,
        gpu_num_filter,
        status_filter,
        latest,
        delete_all,
    )

    if not deployments:
        extra = '' if delete_all else ' matching the specified criteria'
        logger.error(f'{WARN} No deployments found{extra}.')
        return 1
    if not force and not confirm_deployment_update(deployments, 'delete'):
        logger.error(f'{FAIL} Canceling delete deployments')
        return 1

    with console_status('Deleting deployments...'):
        delete_inference_deployments(deployments)

    logger.info(f'{OK} Deleted deployments')
    return 0
