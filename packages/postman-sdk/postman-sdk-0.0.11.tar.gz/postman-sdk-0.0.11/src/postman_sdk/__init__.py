"""
SDK init module
"""
from postman_sdk.model.base_config import PostmanSDKConfig
from postman_sdk.postman_otel.postman_tracer import PostmanTracer


def initialize(config: PostmanSDKConfig):
    """
    Initialize method

    collection_id: str
        The live collection id.

    api_key: str
        Postman API key for authentication.

    enable: Optional[bool] = True
        Enable or disable the SDK. Disabled SDK does not capture any new traces,
        nor does it use up system resources.
        Can be set by using an environment variable 'POSTMAN_SDK_ENABLE',
        which will over-ride any other config.

    debug:  Optional[bool] = False
        Enable debug logs.

    truncate_data: Optional[bool] = True
        Truncate the request and response body so that no PII data is sent to Postman.

        This is **enabled** by default. Disabling it sends actual request and response payloads.

        Example:

        Sample payload or non-truncated payload:
            {
                "first_name": "John",
                "age": 30
            }

        Truncated payload:
            {
                "first_name" : {
                    "type": "str"
                },
                "age": {
                    "type": "int"
                }
            }

    redact_sensitive_data: Optional[DataRedactionConfig]
        Redact sensitive data such as api_keys and auth tokens, before they leave the sdk.

        When this is enabled, below redaction rules are applied by default (they are not case-sensitive):

        {
            "pm_postman_api_key": r"PMAK-[a-f0-9]{24}-[a-f0-9]{34}",
            "pm_postman_access_key": r"PMAT-[0-9a-z]{26}",
            "pm_basic_auth": r"Basic (?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{4}|[A-Za-z0-9+\/]{3}=|[A-Za-z0-9+\/]{2}={2})$",
            "pm_bearer_token": r"Bearer [a-z0-9A-Z\-\._~\+\/]{15,1000}"
        }

        Example:
            {
                "redact_sensitive_data": {
                    "enable": True (default)
                    "rules": {
                        "<rule name>": "<regex to match the rule>", such as
                        "basic_auth": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
                    }
                }
            }

    ignore_incoming_requests: Optional[list]
        List of regexes to be ignored from instrumentation.
        This rule only applies to endpoints that are **served** by the application/server.

        Example:
            {
                "ignore_incoming_requests": ["knockknock", "^get.*"]
            }

            Will ignore any endpoint that contains the work "knockknock" in it, and all endpoints
            that start with get, and contain any characters after that.

    ignore_outgoing_requests: Optional[list]
        List of regexes to be ignored from instrumentation.
        This rule only applies to endpoints that are **called** by the application/server.

        Example:
            {
                "ignore_outgoing_requests": ["knockknock", "^get.*"]
            }

            Will ignore any endpoint that contains the work "knockknock" in it, and all endpoints
            that start with get, and contain any characters after that.

    receiver_base_url: str = DEFAULT_RECEIVER_BASE_URL
        Where the data should be shipped to receiver's http endpoint.
        **Do not override this value**.

    buffer_interval_in_milliseconds: Optional[int] = 5000
        The interval in milliseconds that the SDK waits before sending data to Postman.
        The default interval is 5000 milliseconds. This interval can be tweaked for lower or higher
        throughput systems.
    """

    PostmanTracer(config=config)
