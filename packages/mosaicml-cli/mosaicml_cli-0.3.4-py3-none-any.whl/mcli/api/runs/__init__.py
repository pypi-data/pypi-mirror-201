"""API calls for run management"""
# pylint: disable=useless-import-alias
from mcli.api.model.run import Run
from mcli.api.runs.api_create_run import create_run
from mcli.api.runs.api_delete_runs import delete_run, delete_runs
from mcli.api.runs.api_get_run_logs import follow_run_logs, get_run_logs
from mcli.api.runs.api_get_runs import get_runs
from mcli.api.runs.api_stop_runs import stop_run, stop_runs
from mcli.api.runs.api_watch_run import wait_for_run_status, watch_run_status
from mcli.models import RunConfig
from mcli.utils.utils_run_status import RunStatus

__all__ = [
    'Run',
    'create_run',
    'delete_run',
    'delete_runs',
    'follow_run_logs',
    'get_run_logs',
    'get_runs',
    'stop_run',
    'stop_runs',
    'wait_for_run_status',
    'watch_run_status',
    'RunConfig',
    'RunStatus',
]
