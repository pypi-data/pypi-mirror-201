"""Implementation of mcli get runs"""
from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Generator, List, Optional

from mcli import config
from mcli.api.exceptions import cli_error_handler
from mcli.cli.common.run_filters import configure_submission_filter_argparser, get_runs_with_filters
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay, format_timestamp
from mcli.sdk import Run
from mcli.utils.utils_cli import comma_separated
from mcli.utils.utils_run_status import RunStatus

logger = logging.getLogger(__name__)


class RunColumns(Enum):
    ID = 'id'
    NAME = 'name'
    CLUSTER = 'cluster'
    GPU_TYPE = 'gpu_type'
    GPU_NUM = 'gpu_num'
    CREATED_TIME = 'created_time'
    START_TIME = 'start_time'
    END_TIME = 'end_time'
    USER = 'user'
    STATUS = 'status'


@dataclass
class RunDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run data for display purposes.
    """
    name: str
    gpu_num: str
    created_time: str
    start_time: str
    end_time: str
    status: str
    user: str
    cluster: Optional[str] = None
    gpu_type: Optional[str] = None
    id: Optional[str] = None

    @classmethod
    def from_run(cls, run: Run, include_ids: bool = False) -> RunDisplayItem:
        display_status = run.status.display_name
        if run.reason:
            display_status = f"{display_status} ({run.reason})"
        extracted: Dict[str, str] = {
            RunColumns.NAME.value: run.name,
            RunColumns.CLUSTER.value: run.config.cluster,
            RunColumns.GPU_TYPE.value: run.config.gpu_type or run.config.compute.get('gpu_type', None) or 'Unknown',
            RunColumns.GPU_NUM.value: str(run.config.gpu_num),
            RunColumns.CREATED_TIME.value: format_timestamp(run.created_at),
            RunColumns.START_TIME.value: format_timestamp(run.started_at),
            RunColumns.END_TIME.value: format_timestamp(run.completed_at),
            RunColumns.USER.value: run.created_by,
            RunColumns.STATUS.value: display_status
        }
        if include_ids:
            extracted[RunColumns.ID.value] = run.run_uid

        return RunDisplayItem(**extracted)


# TODO: add column for USER
class MCLIRunDisplay(MCLIGetDisplay):
    """Display manager for runs
    """

    def __init__(self, models: List[Run], include_ids: bool = False):
        self.models = sorted(models, key=lambda x: x.created_at, reverse=True)
        self.include_ids = include_ids

    @property
    def override_column_ordering(self) -> Optional[List[str]]:
        cols = []
        for c in RunColumns:
            if c == RunColumns.NAME:
                continue
            if not self.include_ids and c == RunColumns.ID:
                continue
            cols.append(c.value)
        return cols

    def __iter__(self) -> Generator[RunDisplayItem, None, None]:
        for model in self.models:
            item = RunDisplayItem.from_run(model, include_ids=self.include_ids)
            yield item


@cli_error_handler('mcli get runs')
def cli_get_runs(
    name_filter: Optional[List[str]] = None,
    cluster_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    gpu_type_filter: Optional[List[str]] = None,
    gpu_num_filter: Optional[List[int]] = None,
    status_filter: Optional[List[RunStatus]] = None,
    output: OutputDisplay = OutputDisplay.TABLE,
    include_ids: bool = False,
    latest: bool = False,
    user_filter: Optional[List[str]] = None,
    **kwargs,
) -> int:
    """Get a table of ongoing and completed runs
    """
    del kwargs

    runs = get_runs_with_filters(
        name_filter=name_filter,
        cluster_filter=cluster_filter,
        before_filter=before_filter,
        after_filter=after_filter,
        gpu_type_filter=gpu_type_filter,
        gpu_num_filter=gpu_num_filter,
        status_filter=status_filter,
        latest=latest,
        user_filter=user_filter,
    )

    display = MCLIRunDisplay(runs, include_ids=include_ids)
    display.print(output)

    return 0


def get_runs_argparser(subparsers: argparse._SubParsersAction):
    """Configures the ``mcli get runs`` argparser
    """

    run_examples: str = """Examples:
    $ mcli get runs

    NAME                         CLUSTER    GPU_TYPE      GPU_NUM      CREATED_TIME     USER               STATUS
    run-foo                      c-1        g0-type       8            05/06/22 1:58pm  abc@gmail.com      Completed
    run-bar                      c-2        g0-type       1            05/06/22 1:57pm  abc@gmail.com      Completed

    $ mcli get runs --user xyz@gmail.com
    NAME                         CLUSTER    GPU_TYPE      GPU_NUM      CREATED_TIME     USER               STATUS
    run-xyz-1                    c-1        g0-type       8            05/06/22 1:58pm  xyz@gmail.com      Completed
    run-xyz-2                    c-2        g0-type       1            05/06/22 1:57pm  xyz@gmail.com      Completed
    """
    runs_parser = subparsers.add_parser('runs',
                                        aliases=['run'],
                                        help='Get information on all of your existing runs across all clusters.',
                                        epilog=run_examples,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)

    configure_submission_filter_argparser('get', runs_parser, include_all=False)
    runs_parser.set_defaults(func=cli_get_runs)

    runs_parser.add_argument('--ids',
                             action='store_true',
                             dest='include_ids',
                             default=config.ADMIN_MODE,
                             help='Include the run ids in the output')

    def user(value: str):
        return comma_separated(value)

    runs_parser.add_argument(
        '-u',
        '--user',
        dest='user_filter',
        default=None,
        metavar='User',
        type=user,
        help='Fetch the runs created by a user in your organization with their email address. '
        'Multiple users should be specified using a comma-separated list, '
        'e.g. "alice@gmail.com,bob@gmail.com"',
    )
    return runs_parser
