"""
Defaults constants
"""

HEALTH_CHECK_ERROR_COUNT_THRESHOLD = 5
HTTP_STATUS_OK = 200
# TODO: decide proper timeout values
HTTP_REQUEST_CONNECTION_TIMEOUT = 6  # must be > multiples of 3
HTTP_REQUEST_READ_TIMEOUT = 30  # must be > multiples of 3
HTTP_REQUEST_TIMEOUT = (HTTP_REQUEST_CONNECTION_TIMEOUT, HTTP_REQUEST_READ_TIMEOUT)
DEFAULT_IGNORED_HOSTNAMES = [
    "newrelic.com",
]
POSTMAN_TELEMETRY = "postman-sdk"
POSTMAN_COLLECTION_ID = "postman.collection.id"
POSTMAN_SDK_VERSION = "postman.sdk.version"
DEFAULT_RECEIVER_BASE_URL = "https://trace-receiver.postman.com"
X_API_KEY = "x-api-key"
CONTENT_TYPE = "Content-type"

# DataTruncation constants


DEFAULT_TRUNCATION_MAX_DEPTH = 2
TRUNCATION_START_LEVEL = 1
POSTMAN_SDK_ENABLE_FLAG = "POSTMAN_SDK_ENABLE"
