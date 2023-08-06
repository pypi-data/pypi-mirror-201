"""
Instrumentation for Python `requests` library.
"""
import json
from typing import Optional

from postman_sdk.instrumentor.base_instrumentation import (
    HttpInstrumentationBase,
    BaseResponse,
    BaseRequest,
)
from postman_sdk.util.helper import unpack_url
from postman_sdk.util.logger import _LOG


class RequestsInstrumentation(HttpInstrumentationBase):
    """
    Requests Instrumentation module
    """

    def __init__(
        self,
        tracer_provider,
        ignore_outgoing_requests: Optional[str] = None,
        *args,
        **kwargs,
    ):
        module_name = "RequestsInstrumentor"
        try:
            super().__init__(
                opentelemetry_package="opentelemetry.instrumentation.requests",
                module_name=module_name,
            )

            self.instrumented_instance = self.instrumentor_class().instrument(
                trace_provider=tracer_provider,
                span_callback=self.span_callback,
                excluded_urls=ignore_outgoing_requests,
            )
        except ModuleNotFoundError:
            _LOG.warning(f"Postman: skipping instrumenting {module_name}")

    @staticmethod
    def span_callback(span, http_object):
        """
        call back method to requests instrumentor.
        :param span
        :param http_object
        """
        if not http_object:
            _LOG.info("Postman: Requests instrumentation empty object on callback.")

            return
        if hasattr(http_object, "request"):
            request = BaseRequest()
            body = {}

            try:
                body = http_object.request.json
            except:
                body = {}

            request.body = json.dumps(body)

            request.headers = json.dumps(dict(http_object.request.headers))
            url_object = unpack_url(http_object.request.url)
            request.route = url_object["target"]
            request.query = url_object["query"]

            RequestsInstrumentation.set_attributes(span, request)

        # Response part of the requests
        if hasattr(http_object, "raw"):
            response = BaseResponse()
            response.headers = json.dumps(dict(http_object.raw.headers))
            response.body = http_object.text

            RequestsInstrumentation.set_attributes(span, response)
