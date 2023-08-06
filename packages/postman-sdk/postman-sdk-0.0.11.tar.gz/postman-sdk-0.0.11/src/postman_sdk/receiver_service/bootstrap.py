import backoff
from http import HTTPStatus

from postman_sdk.receiver_service import BOOTSTRAP_PATH
from postman_sdk.receiver_service.client import call_reciever_api
from postman_sdk.receiver_service.config import BOOTSTRAP_RETRY_COUNT
from postman_sdk.model.base_config import BaseConfig


def is_retryable(resp) -> bool:
    if not hasattr(resp, "status_code"):
        return False
    return resp.status_code in [
        HTTPStatus.CONFLICT.value,
        HTTPStatus.INTERNAL_SERVER_ERROR.value,
        HTTPStatus.GATEWAY_TIMEOUT.value,
        HTTPStatus.SERVICE_UNAVAILABLE.value,
        HTTPStatus.BAD_GATEWAY.value,
    ]


def is_success(resp) -> bool:
    return resp.status_code == HTTPStatus.OK.value and "currentConfig" in resp.json()


@backoff.on_predicate(
    backoff.expo,
    predicate=is_retryable,
    max_tries=BOOTSTRAP_RETRY_COUNT,
)
def bootstrapSDK(config: BaseConfig):
    """
    method to call Bootstrap endpoint. Raises error if bootstrap errors.
    :param config:
    :return: None
    """

    payload = {
        "sdk": {"collectionId": f"{config.collection_id}", "enabled": config.enable}
    }
    resp = call_reciever_api(config=config, path=BOOTSTRAP_PATH, payload=payload)

    return resp
