"""mcli predict entrypoint"""
import argparse
import logging
from pprint import pprint
from typing import Any, Dict, Optional

import yaml

from mcli.api.exceptions import MAPIException
from mcli.cli.common.deployment_filters import get_deployments_with_filters
from mcli.sdk import predict
from mcli.utils.utils_logging import FAIL, err_console

logger = logging.getLogger(__name__)


def predict_cli(
    inputs: Dict[str, Any],
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
                err_console.print(f'No inference deployment found with name {deployment_name}.')
            return 1

        resp = predict(deployments[0], inputs=inputs)
        print(f'{deployments[0].name}\'s prediction results:')
        pprint(resp)
        return 0
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MAPIException as e:
        logger.error(f'{FAIL} {e}')
        return 1


def add_predict_parser(subparser: argparse._SubParsersAction):
    predict_parser: argparse.ArgumentParser = subparser.add_parser(
        'predict',
        help='Run prediction on a model in the MosaicML Cloud with given inputs. Returns forward pass result',
    )
    predict_parser.add_argument('deployment_name',
                                metavar='DEPLOYMENT',
                                nargs='?',
                                help='The name of the deployment to run inference on')

    predict_parser.add_argument(
        '--input',
        '--inputs',
        '-i',
        dest='inputs',
        required=True,
        nargs="?",
        type=yaml.safe_load,
        metavar='INPUT',
        help='Input values to run forward pass on. Input values must be JSON-serializable and have string keys.',
    )

    predict_parser.set_defaults(func=predict_cli)
