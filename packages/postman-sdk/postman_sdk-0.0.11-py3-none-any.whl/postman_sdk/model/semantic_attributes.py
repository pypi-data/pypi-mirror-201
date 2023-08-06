"""
Module for adding all custom span keys
"""


class HTTPSpanAttributes:
    """
    Http span attributed Semantic module.
    """

    HTTP_REQUEST_BODY = "http.request.body"
    HTTP_REQUEST_HEADERS = "http.request.headers"
    HTTP_REQUEST_PARAMS = "http.request.params"
    HTTP_REQUEST_QUERY = "http.request.query"
    HTTP_ROUTE = "http.route"
    HTTP_RESPONSE_HEADERS = "http.response.headers"
    HTTP_RESPONSE_BODY = "http.response.body"
