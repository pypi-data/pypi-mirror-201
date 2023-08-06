"""
Data tool provided redaction and truncation.
"""
from postman_sdk.plugins.data_redaction import DataRedactor
from postman_sdk.plugins.data_truncation import (
    DataTruncation,
    DEFAULT_TRUNCATION_MAX_DEPTH,
)

HTTP_REQUEST_KEYS = {"uri": "http.target", "method": "http.method"}

DEFAULT_REDACTION_REPLACEMENT_STRING = "************"

DEFAULT_REDACTION_RULES = {
    "pm_postman_api_key": r"PMAK-[a-f0-9]{24}-[a-f0-9]{34}",
    "pm_postman_access_key": r"PMAT-[0-9a-z]{26}",
    "pm_basic_auth": r"Basic (?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{4}|[A-Za-z0-9+\/]{3}=|[A-Za-z0-9+\/]{2}={2})$",
    "pm_bearer_token": r"Bearer [a-z0-9A-Z\-\._~\+\/]{15,1000}",
}

HTTP_ATTRIBUTES__REQUEST_REDACTION_MAP = {
    "body": {
        "attribute_key": "http.request.body",
        "redaction_function": "redact_body_data",
    },
    "headers": {
        "attribute_key": "http.request.headers",
        "redaction_function": "redact_headers_data",
    },
    "queryUrl": {
        "attribute_key": "http.url",
        "redaction_function": "redact_uristring_data",
    },
    "queryString": {
        "attribute_key": "http.request.query",
        "redaction_function": "redact_query_data",
    },
    "targetUrl": {
        "attribute_key": "http.target",
        "redaction_function": "redact_uristring_data",
    },
}
HTTP_ATTRIBUTES__RESPONSE_REDACTION_MAP = {
    "body": {
        "attribute_key": "http.response.body",
        "redaction_function": "redact_body_data",
    },
    "headers": {
        "attribute_key": "http.response.headers",
        "redaction_function": "redact_headers_data",
    },
}

POSTMAN_DATA_REDACTION_FLAG_ATTRIBUTE_NAME = "postman.dataRedaction"
POSTMAN_REDACTED_ATTRIBUTE_NAME = "postman.redacted"
POSTMAN_DATA_TRUNCATION_ATTRIBUTE_NAME = "postman.dataTruncated"

SPAN_HTTP_BODY_ATTRIBUTES_NAMES = {
    "response": "http.response.body",
    "request": "http.request.body",
}

DATA_REDACTION_PLUGIN_NAMESPACE = "redact_sensitive_data"
DATA_TRUNCATION_PLUGIN_NAMESPACE = "truncate_data"

PLUGINS = {
    DATA_REDACTION_PLUGIN_NAMESPACE: {
        "function": DataRedactor,
        "config_attributes": [
            {
                "name": "redact_sensitive_data",
                "function_arg": "redaction_rules",
                "default": {},
            }
        ],
    },
    DATA_TRUNCATION_PLUGIN_NAMESPACE: {
        "function": DataTruncation,
        "config_attributes": [
            {
                "name": "truncation_max_depth",
                "function_arg": "max_depth",
                "default": DEFAULT_TRUNCATION_MAX_DEPTH,
            }
        ],
    },
}
