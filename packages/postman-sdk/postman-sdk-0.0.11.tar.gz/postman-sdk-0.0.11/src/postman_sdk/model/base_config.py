"""
Provide basic config structure
"""
# pylint:disable=E0611,R0903
from typing import Optional, List

try:
    from typing_extensions import TypedDict
except ImportError:
    from typing import TypedDict

from pydantic import BaseModel

from postman_sdk.model.data_redaction import DataRedactionConfig
from postman_sdk.util.constants import DEFAULT_RECEIVER_BASE_URL


class BaseConfig(BaseModel):
    """
    Base config class
    """

    collection_id: str
    receiver_base_url: str = DEFAULT_RECEIVER_BASE_URL
    enable: Optional[bool] = True
    buffer_interval_in_milliseconds: Optional[int]
    api_key: str
    debug: Optional[bool] = False
    truncate_data: Optional[bool] = True
    redact_sensitive_data: Optional[DataRedactionConfig]
    ignore_outgoing_requests: Optional[List[str]]
    ignore_incoming_requests: Optional[List[str]]


class PostmanSDKConfig(TypedDict, total=False):
    """
    Typed Dict representation of the above BaseConfig.
    This is required to allow for a more UX friendly onboarding for the users.
    """

    collection_id: str
    api_key: str
    enable: Optional[bool]
    debug: Optional[bool]
    truncate_data: Optional[bool]
    redact_sensitive_data: Optional[DataRedactionConfig]
    ignore_incoming_requests: Optional[List[str]]
    ignore_outgoing_requests: Optional[List[str]]
    receiver_base_url: Optional[str]
    buffer_interval_in_milliseconds: Optional[int]
