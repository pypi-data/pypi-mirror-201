"""
Module for Flask Instrumentation, will relay on open-telemetry.instrumentation.flask
"""
import json

# pylint:disable=W0718,W0613,C0123
from typing import Dict, Optional

import wrapt
from opentelemetry.sdk.trace import Span
from opentelemetry.trace import get_current_span
from postman_sdk.instrumentor.base_instrumentation import (
    HttpInstrumentationBase,
    BaseResponse,
    BaseRequest,
)
from postman_sdk.util.logger import _LOG

REQUEST_ATTRIBUTE = "request_object"


class FlaskInstrumentation(HttpInstrumentationBase):
    """
    Class for FlaskInstrumentation
    """

    FLASK_REQUEST_VAR_NAME = "werkzeug.request"

    def __init__(
        self,
        tracer_provider,
        ignore_incoming_requests: Optional[str] = None,
        *args,
        **kwargs,
    ):
        self.instrumented_instance = None
        self.tracer_provider = tracer_provider
        self.ignore_incoming_requests = ignore_incoming_requests
        module = "FlaskInstrumentor"

        try:
            super().__init__(
                opentelemetry_package="opentelemetry.instrumentation.flask",
                module_name=module,
            )

            wrapt.wrap_function_wrapper(
                "flask", "Flask.__init__", self._patch_instance_for_instrumentation
            )
        except ModuleNotFoundError:
            _LOG.warning(f"Postman: skipping instrumenting {module}")

    @staticmethod
    def request_hook(span: Span, flask_request_environ: Dict) -> None:
        """
        Request hook for flask
        :param span:
        :param flask_request_environ:
        :return:
        """
        if span is None:
            return

        try:
            request = flask_request_environ.get(
                FlaskInstrumentation.FLASK_REQUEST_VAR_NAME
            )
            request_object = BaseRequest()

            try:
                request_object.body = request.json
            except:
                request_object.body = {}

            request_object.body = json.dumps(request_object.body)
            request_object.headers = json.dumps(dict(request.headers))
            request_object.params = json.dumps(request.view_args)
            request_object.query = json.dumps(request.args)

            FlaskInstrumentation.set_attributes(span, request_object)

        except Exception as error:  # TODO fine tune error catching.
            _LOG.debug("Flask request instrumentation error: %s", error)

    @staticmethod
    def flask_response_callback(response):
        """
        Callback for flask to call before the request.
        :param response:
        :return:
        """
        span = get_current_span()
        if not span:
            _LOG.debug("Failed to get the current span.")
            return None

        try:
            response_object = BaseResponse()
            response_object.body = (
                json.dumps(response.json) if response.is_json else "{}"
            )
            response_object.headers = json.dumps(dict(response.headers))

            FlaskInstrumentation.set_attributes(span=span, http_object=response_object)
        except Exception as error:
            _LOG.debug(f"Flask after_request instrumentation error: {error}")

        return response

    def _patch_instance_for_instrumentation(self, wrapped, instance, args, kwargs):
        res = wrapped(*args, **kwargs)

        # wrapping.
        try:
            if not self.instrumented_instance:
                self.instrumented_instance = self.instrumentor_class().instrument_app(
                    instance,
                    tracer_provider=self.tracer_provider,
                    request_hook=self.request_hook,
                    excluded_urls=self.ignore_incoming_requests,
                )

                instance.after_request(self.flask_response_callback)

        except Exception as error:
            _LOG.debug(f"Flask __init__ instrumentation error: {error}.")

        return res
