""" Ping a InferenceDeployment """
from __future__ import annotations

from typing import Optional

import requests
from requests import Response

from mcli.api.model.inference_deployment import InferenceDeployment

__all__ = ['ping_inference_deployment']


def ping_inference_deployment(
    deployment: InferenceDeployment,
    timeout: Optional[float] = 10,
) -> dict:
    """Pings an inference deployment that has been launched in the MosaicML platform
    and returns the status of the deployment. The deployment must have a '/ping' endpoint
    defined.
    Arguments:
        deployment: Inference deployment to ping for a status check
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised.
    Raises:
        HTTPError: If pinging the endpoint fails
    """
    # Fallback needed for backward compatibility
    url = deployment.public_dns or deployment.get_inference_deployment_address()
    resp: Response = requests.get(url=url + '/ping', timeout=timeout)
    if resp.ok:
        return resp.json()
    else:
        resp.raise_for_status()
        return {}
