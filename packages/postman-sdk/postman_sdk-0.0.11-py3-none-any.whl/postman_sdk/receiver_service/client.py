import json
import requests
from http import HTTPStatus

from postman_sdk.util.constants import (
    X_API_KEY,
    CONTENT_TYPE,
)
from postman_sdk.util.logger import _LOG
from postman_sdk.model.base_config import BaseConfig
from postman_sdk.model.http import EmptyResponse
from postman_sdk.util.constants import HTTP_REQUEST_TIMEOUT


def call_reciever_api(config: BaseConfig, path: str, payload: dict):
    """
    Method to call reciever service APIs
    :param config:
    :return: None
    """
    resp = None
    headers = {X_API_KEY: config.api_key, CONTENT_TYPE: "application/json"}
    api_url = f"{config.receiver_base_url}{path}"

    try:
        resp = requests.post(
            api_url,
            data=json.dumps(payload),
            headers=headers,
            timeout=HTTP_REQUEST_TIMEOUT,
        )
        _LOG.debug(
            f"Tracer service called path: {path}, status_code:"
            f" {resp.status_code}, body: {resp.json()}"
        )
    except Exception as e:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
        if resp is not None and hasattr(resp, "status_code"):
            status_code = resp.status_code
        resp = EmptyResponse(status_code=status_code, data={"message": str(e)})
        _LOG.debug(
            f"Tracer service called path: {path}, status_code:{resp.status_code},"
            f" body: {resp.json()}"
        )
    return resp
