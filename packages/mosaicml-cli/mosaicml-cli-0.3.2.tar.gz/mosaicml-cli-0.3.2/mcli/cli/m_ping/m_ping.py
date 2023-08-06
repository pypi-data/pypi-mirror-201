""" mcli ping entrypoint """
import argparse
import logging
from pprint import pprint
from typing import Optional

from mcli.api.exceptions import MAPIException
from mcli.cli.common.deployment_filters import get_deployments_with_filters
from mcli.sdk import ping_inference_deployment
from mcli.utils.utils_logging import FAIL, err_console

logger = logging.getLogger(__name__)


def ping(
    deployment_name: Optional[str] = None,
    **kwargs,
) -> int:
    del kwargs
    try:
        name_filter = [deployment_name] if deployment_name else None
        deployments = get_deployments_with_filters(name_filter=name_filter, latest=True)

        if len(deployments) == 0:
            if not deployment_name:
                err_console.print("No inference deployments found.")
            else:
                err_console.log(f'No inference deployment foung with name {deployment_name}.')
            return 1

        resp = ping_inference_deployment(deployments[0])
        print(f'{deployments[0].name}\'s status:')
        pprint(resp)
        return 0
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except (MAPIException) as e:
        logger.error(f'{FAIL} {e}')
        return 1


def add_ping_parser(subparser: argparse._SubParsersAction):
    ping_parser: argparse.ArgumentParser = subparser.add_parser(
        'ping',
        help='Ping a inference deployment in the MosaicML platform for health metrics',
    )
    ping_parser.add_argument(
        'inference_deployment_name',
        metavar='DEPLOYMENT',
        nargs='?',
        help='The name of the inference deployment. If not provided, will return the metrics of the latest deployment')

    ping_parser.set_defaults(func=ping)
