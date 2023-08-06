"""
SDK initializer.
"""
# pylint:disable=W0622,R0913
# system imports
try:
    from importlib_metadata import version
except ImportError:
    from importlib.metadata import version
import os
from typing import Union, Dict


# open-telemetry imports
from opentelemetry import trace
from opentelemetry.instrumentation.propagators import (
    set_global_response_propagator,
    TraceResponsePropagator,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.resource import ResourceAttributes
from pydantic import ValidationError

from postman_sdk.instrumentor import get_instrumentations
from postman_sdk.model.base_config import BaseConfig, PostmanSDKConfig
from postman_sdk.postman_otel.postman_exporter import PostmanSpanExporter
from postman_sdk.receiver_service import HealthCheck, TRACE_RECEIVER_PATH
from postman_sdk.receiver_service import bootstrap
from postman_sdk.util.constants import (
    POSTMAN_SDK_VERSION,
    POSTMAN_COLLECTION_ID,
    POSTMAN_TELEMETRY,
    X_API_KEY,
    POSTMAN_SDK_ENABLE_FLAG,
)
from postman_sdk.util.helper import add_postman_excluded_urls, add_user_excluded_urls
from postman_sdk.util.logger import set_log_level, _LOG


class PostmanTracer:
    """
    PostmanTracer class, that initializes otel instrumentation.
    """

    __provider: TracerProvider
    config: BaseConfig
    tracing_suppressed = False

    def __init__(self, config: Union[Dict, PostmanSDKConfig]):
        """
        initialize
        * Tracer
        * Adds SpanProcessor
        """
        try:
            self.__parse_config(config)
        except ValidationError as config_error:
            _LOG.error(f"Unable to parse configuration \n error: {config_error}")
            _LOG.warning("Postman SDK Disbaled")

            return

        set_log_level(log_level="DEBUG" if self.config.debug else "ERROR")

        POSTMAN_SDK_ENABLE = os.environ.get(POSTMAN_SDK_ENABLE_FLAG, "")

        if POSTMAN_SDK_ENABLE.lower() == "true":
            self.config.enable = True
        elif POSTMAN_SDK_ENABLE.lower() == "false":
            self.config.enable = False

        if not self.config.enable:
            _LOG.error("Postman SDK Disabled")

            return

        resource = {}

        if not self.bootstrap_sdk():
            return

        HealthCheck(self).run()

        self.__update_resource_tags(resource, self.config)

        set_global_response_propagator(TraceResponsePropagator())
        self.__provider = TracerProvider(resource=Resource.create(resource))
        trace.set_tracer_provider(self.__provider)

        exporter = self.get_otlp_exporter(self.config)

        self.__provider.add_span_processor(
            BatchSpanProcessor(
                span_exporter=exporter,
                schedule_delay_millis=self.config.buffer_interval_in_milliseconds,
            )
        )

        get_instrumentations(
            tracer_provider=self.__provider,
            ignore_outgoing_requests=add_postman_excluded_urls(self.config),
            ignore_incoming_requests=add_user_excluded_urls(
                self.config.ignore_incoming_requests
            ),
        )

        _LOG.error("Postman SDK Instrumentation successful !!")

    def bootstrap_sdk(self) -> bool:
        response = bootstrap.bootstrapSDK(self.config)
        if not bootstrap.is_success(response):
            _LOG.error("Postman SDK disabled")
            self.disable()

            return False

        self.config.enable = (
            response.json().get("currentConfig", {}).get("enabled", False)
        )

        if not self.config.enable:
            self.suppress()
        else:
            self.unsuppress()

        return True

    @staticmethod
    def get_otlp_exporter(config: BaseConfig) -> PostmanSpanExporter:
        """
        Create Span exporter and return.
        :param config: BaseConfig
        :return: PostmanSpanExporter object.
        """
        endpoint = f"{config.receiver_base_url}{TRACE_RECEIVER_PATH}"
        headers = {
            X_API_KEY: config.api_key,
        }

        return PostmanSpanExporter(
            endpoint=endpoint,
            headers=headers,
            config=config,
            postman_tracer=PostmanTracer,
        )

    @staticmethod
    def __update_resource_tags(resource_tags, config: BaseConfig):
        """
        Method to add resource tags.
        :return:
        """
        resource_tags.update(
            {
                ResourceAttributes.TELEMETRY_SDK_NAME: POSTMAN_TELEMETRY,
                POSTMAN_COLLECTION_ID: config.collection_id,
                POSTMAN_SDK_VERSION: version("postman-sdk"),
            }
        )

    def __parse_config(self, config):
        """
        Method to parse config to BaseConfig
        :param config:
        :return:
        """
        self.config = BaseConfig(**config)

        if self.config.receiver_base_url.endswith("/"):
            self.config.receiver_base_url = self.config.receiver_base_url[:-1]

    @staticmethod
    def suppress():
        _LOG.debug("Postman SDK Disabling tracing")
        PostmanTracer.tracing_suppressed = True

    @staticmethod
    def unsuppress():
        _LOG.debug("Postman SDK Enabling Tracing")
        PostmanTracer.tracing_suppressed = False

    @staticmethod
    def is_suppressed():
        return PostmanTracer.tracing_suppressed

    @staticmethod
    def disable():
        PostmanTracer.suppress()
        # TODO: Is this needed ?
        # since we've solved disabling from HealthCheck._health_poller()
        # PostmanTracer.disable_health_check()
