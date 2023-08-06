"""Implementation of mcli describe run"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Generator, List, Optional, Tuple

from rich.table import Table

from mcli.api.exceptions import KubernetesException, MAPIException
from mcli.api.model.run import Node, Run
from mcli.cli.m_get.display import (MCLIDisplayItem, MCLIGetDisplay, OutputDisplay, create_vertical_display_table,
                                    format_timestamp)
from mcli.config import MESSAGE, MCLIConfigError
from mcli.sdk import get_runs
from mcli.utils.utils_logging import FAIL, FormatString, format_string, print_timedelta

logger = logging.getLogger(__name__)

DISPLAY_RUN_STATUSES = ['PENDING', 'RUNNING', 'COMPLETED']


class DisplayRunStatus(Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'


class DescribeRunMetadataColumns(Enum):
    NAME = 'name'
    RUN_ID = 'run_uid'
    CLUSTER = 'cluster'
    GPU_TYPE = 'gpu_type'
    GPU_NUM = 'gpu_num'
    CPUS = 'cpus'
    IMAGE = 'image'


class DescribeRunLifecycleColumns(Enum):
    STATUS = 'status'
    START_TIME = 'start_time'
    END_TIME = 'end_time'
    DURATION = 'duration'


class DescribeRunOriginalInputColumns(Enum):
    SUBMITTED_CONFIG = 'submitted_config'


RUN_METADATA_DISPLAY_NAMES = ['Run Name', 'Cluster', 'Image', 'GPU Type', 'GPU Num']

RUN_LIFECYCLE_DISPLAY_NAMES = [
    'Start Time',
    'End Time',
    'Duration',
]
RUN_NODES_DISPLAY_NAMES = ['Node Name']
SUBMITTED_CONFIG = ['Run Config']


@dataclass
class DescribeRunMetadataDisplayItem(MCLIDisplayItem):
    """Tuple that extracts detailed run data for display purposes"""
    name: str
    cluster: str
    image: str
    gpu_type: Optional[str] = None
    gpu_num: Optional[str] = None

    @classmethod
    def from_run(cls, run: Run) -> DescribeRunMetadataDisplayItem:
        extracted: Dict[str, Any] = {
            DescribeRunMetadataColumns.NAME.value: run.config.name,
            DescribeRunMetadataColumns.CLUSTER.value: run.config.cluster,
            DescribeRunMetadataColumns.IMAGE.value: run.config.image,
            DescribeRunMetadataColumns.GPU_TYPE.value: run.config.gpu_type,
            DescribeRunMetadataColumns.GPU_NUM.value: run.config.gpu_num,
        }

        return DescribeRunMetadataDisplayItem(**extracted)


@dataclass
class DescribeRunLifecycleDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run data for run lifecycle display purposes"""
    status: str
    start_time: str
    end_time: str
    duration: str


@dataclass
class MCLIDescribeRunNodeDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run data for run node display purposes"""
    rank: int
    name: str


# Displays
class MCLIDescribeRunMetadataDisplay(MCLIGetDisplay):
    """ Vertical table view of run metadata """

    def __init__(self, models: List[Run]):
        self.models = sorted(models, key=lambda x: x.created_at, reverse=True)

    @property
    def index_label(self) -> str:
        return ""

    def create_custom_table(self, columns: List[str], data: List[Tuple[Any, ...]], names: List[str]) -> Optional[Table]:
        return create_vertical_display_table(data=data, columns=RUN_METADATA_DISPLAY_NAMES)

    def __iter__(self) -> Generator[DescribeRunMetadataDisplayItem, None, None]:
        for model in self.models:
            item = DescribeRunMetadataDisplayItem.from_run(model)
            yield item


class MCLIDescribeRunLifecycleDisplay(MCLIGetDisplay):
    """ Horizontal table view of run lifecycle """

    def __init__(self, models: List[Run]):
        self.model = models[0]

    @property
    def custom_column_names(self) -> List[str]:
        return RUN_LIFECYCLE_DISPLAY_NAMES

    def __iter__(self) -> Generator[DescribeRunLifecycleDisplayItem, None, None]:
        for e in DisplayRunStatus:
            item = format_run_status(e.value, self.model)
            yield item

    @property
    def index_label(self) -> str:
        return 'status'


class MCLIDescribeRunNodeDisplay(MCLIGetDisplay):
    """ Horizontal table view of run node """

    def __init__(self, nodes: List[Node]):
        self.nodes = sorted(nodes, key=lambda x: x.rank)

    @property
    def custom_column_names(self) -> List[str]:
        return RUN_NODES_DISPLAY_NAMES

    def __iter__(self) -> Generator[MCLIDescribeRunNodeDisplayItem, None, None]:
        for n in self.nodes:
            yield MCLIDescribeRunNodeDisplayItem(n.rank, n.name)

    @property
    def index_label(self) -> str:
        return 'rank'


# Run lifecycle


def format_run_status(status: str, run: Run) -> DescribeRunLifecycleDisplayItem:
    if status == DisplayRunStatus.PENDING.value:
        duration = print_timedelta(run.started_at - run.created_at) if run.started_at and run.created_at else '-'
        return DescribeRunLifecycleDisplayItem(status=status,
                                               start_time=format_timestamp(run.created_at),
                                               end_time=format_timestamp(run.started_at),
                                               duration=duration)
    elif status == DisplayRunStatus.RUNNING.value:
        duration = print_timedelta(run.completed_at - run.started_at) if run.completed_at and run.started_at else '-'
        return DescribeRunLifecycleDisplayItem(status=status,
                                               start_time=format_timestamp(run.started_at),
                                               end_time=format_timestamp(run.completed_at),
                                               duration=duration)
    else:
        return DescribeRunLifecycleDisplayItem(status=status,
                                               start_time=format_timestamp(run.completed_at),
                                               end_time='--',
                                               duration='')


# Original run input


def describe_run(run_name: str, output: OutputDisplay = OutputDisplay.TABLE, **kwargs):
    """
    Fetches more details of a Run
    """
    del kwargs

    runs: List[Run] = []
    try:
        runs = get_runs(runs=[run_name], timeout=None)
    except (KubernetesException, MAPIException, RuntimeError) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)

    if len(runs) == 0:
        logger.error(f'No runs found for name: {run_name}')
        return

    run: Run = runs[0]
    # Run metadata section
    print(format_string('Run Metadata', FormatString.BOLD))
    metadata_display = MCLIDescribeRunMetadataDisplay([run])
    metadata_display.print(output)
    print()

    # Run lifecycle section
    print(format_string('Run Lifecycle', FormatString.BOLD))
    lifecycle_display = MCLIDescribeRunLifecycleDisplay([run])
    lifecycle_display.print(output)
    print()

    if run.nodes:
        print(format_string('Run Nodes', FormatString.BOLD))
        node_display = MCLIDescribeRunNodeDisplay(run.nodes)
        node_display.print(output)
        print()

    # Run original input section
    print(format_string('Submitted YAML', FormatString.BOLD))
    print(run.submitted_config)

    # TODO: cleanup code to print directly to console after parsing
    # wrap command string within a literal `representer` - dump long str as block
