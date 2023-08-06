""" Predict on an Inference Deployment """
from __future__ import annotations

from typing import Any, Dict, Optional

import requests
from requests import Response

from mcli.api.model.inference_deployment import InferenceDeployment

__all__ = ['predict']


def predict(
    deployment: InferenceDeployment,
    inputs: Dict[str, Any],
    timeout: Optional[float] = 20,
) -> dict:
    """Sends input to \'/infer\' endpoint of an inference deployment on the MosaicML
    platform. Runs prediction on input and returns output produced by the model.
    Arguments:
        deployment: Inference deployment to send input to
        input: Input data to run prediction on in the form of dictionary
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised.
    Raises:
        HTTPError: If sending the request to the endpoint fails
    """
    # Fallback needed for backward compatibility until public_dns is written to the DB
    url = deployment.public_dns or deployment.get_inference_deployment_address()
    resp: Response = requests.post(url=url + '/infer', timeout=timeout, json=inputs)
    if resp.ok:
        return resp.json()
    else:
        resp.raise_for_status()
        return {}
