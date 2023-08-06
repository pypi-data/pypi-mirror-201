"""
Base HTTP instrumentation module, this module will handle setting attributes on spans.
Initializing the passed Frameworks.
"""
from importlib import import_module
from typing import Union

from opentelemetry.sdk.trace import Span

from postman_sdk.model.semantic_attributes import HTTPSpanAttributes


class BaseRequest:
    """
    Basic Request structure for common http spans
    """

    body: str = ""
    headers: str = ""
    params: str = ""
    query: str = ""
    route: str = ""


class BaseResponse:
    """
    Basic Response structure for common http spans
    """

    body: str = ""
    headers: str = ""


class HttpInstrumentationBase:
    """
    Basic framework for HTTP based instrumentation
    """

    def __init__(self, opentelemetry_package: str, module_name: str):
        """
        HttpInstrumentationBase, takes opentelemetry_package and module name to facilitate dynamic loading.
        """
        self.instrumentor_class = None
        self.import_and_set_instrumentor_class(opentelemetry_package, module_name)

    @staticmethod
    def set_attributes(span: Span, http_object: Union[BaseRequest, BaseResponse]):
        """
        Method to set attributed on Span for Request and Response sections.
        """
        if isinstance(http_object, BaseRequest):
            span.set_attributes(
                {
                    HTTPSpanAttributes.HTTP_REQUEST_BODY: http_object.body,
                    HTTPSpanAttributes.HTTP_REQUEST_HEADERS: http_object.headers,
                    HTTPSpanAttributes.HTTP_REQUEST_PARAMS: http_object.params,
                    HTTPSpanAttributes.HTTP_REQUEST_QUERY: http_object.query,
                    # url_rule is None in case of 404
                    HTTPSpanAttributes.HTTP_ROUTE: http_object.route,
                }
            )
        elif isinstance(http_object, BaseResponse):
            span.set_attributes(
                {
                    HTTPSpanAttributes.HTTP_RESPONSE_HEADERS: http_object.headers,
                    HTTPSpanAttributes.HTTP_RESPONSE_BODY: http_object.body,
                }
            )

    def import_and_set_instrumentor_class(self, opentelemetry_package, module_name):
        """
        Method to call the instrumentor class as member of HttpInstrumentationBase.
        """
        self.instrumentor_class = getattr(
            import_module(opentelemetry_package), module_name
        )
