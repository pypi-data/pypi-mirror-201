"""
Module to customize SpanExporter
"""
import json
from collections import OrderedDict
from google.protobuf.json_format import MessageToDict
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
)
from postman_sdk.model.base_config import BaseConfig
from postman_sdk.model.http import EmptyResponse
from postman_sdk.plugins import (
    DATA_REDACTION_PLUGIN_NAMESPACE,
    DATA_TRUNCATION_PLUGIN_NAMESPACE,
    POSTMAN_DATA_TRUNCATION_ATTRIBUTE_NAME,
    POSTMAN_DATA_REDACTION_FLAG_ATTRIBUTE_NAME,
)

from postman_sdk.util.logger import _LOG

_OTL_JSON_CONTENT_HEADER = {"Content-Type": "application/json"}


class PostmanSpanExporter(OTLPSpanExporter):
    """
    Implementation of SpanExporter.
    """

    def __init__(self, *args, **kwargs):
        """
        exporter init.
        """
        self.postman_tracer = kwargs.pop("postman_tracer")
        self.config = kwargs.pop("config")
        self.plugins = OrderedDict()

        if self.config.truncate_data:
            self.load_plugin(DATA_TRUNCATION_PLUGIN_NAMESPACE, self.config)

        redaction_config = self.config.redact_sensitive_data

        if redaction_config and redaction_config.enable:
            self.load_plugin(DATA_REDACTION_PLUGIN_NAMESPACE, self.config)

        super().__init__(*args, **kwargs)

    def load_plugin(self, plugin_name: str, config: BaseConfig):
        """
        Method to load span hooks
        :param plugins:
        :return:
        """

        from postman_sdk.plugins import PLUGINS

        plugin = PLUGINS.get(plugin_name)

        if not plugin:
            _LOG.error(
                f"Invalid plugin: {plugin_name}, should be one of"
                f" {', '.join(PLUGINS.keys())}"
            )

            return

        func_config = {}

        for config_attrs in plugin["config_attributes"]:
            func_config[config_attrs["function_arg"]] = getattr(
                config,
                config_attrs["name"],
                config_attrs["default"],
            )

        self.plugins[plugin_name] = plugin["function"](**func_config)

    def run_plugins(self, spans) -> list:
        """
        Apply plugins on spans.
        :param spans:
        :return: list of spans.
        """
        for span_idx, span in enumerate(spans):
            for plugin_name, plugin in self.plugins.items():
                _LOG.info(f"Running plugin in span: {plugin_name}")

                try:
                    """
                    Structure of span.get("attributes") is:
                    [
                        {
                            "key": "http.request.body",
                            "value": {"stringValue": "<json-dumped-body-here>"},
                        }
                    ]
                    """
                    span_attributes = span.get("attributes", [])

                    """
                    parsed_attributes = {
                        "http.request.body": {"stringValue": "<body>"}
                    }
                    """
                    parsed_attributes = {
                        item["key"]: item["value"] for item in span_attributes
                    }
                    """
                    plugin_attributes = {
                        "http.request.body": "<body>"
                    }
                    """
                    plugin_attributes = {
                        key: value[list(value.keys())[0]]
                        for key, value in parsed_attributes.items()
                    }

                    _attributes = plugin.run(plugin_attributes)
                    if _attributes:
                        parsed_attributes = {
                            key: {list(value.keys())[0]: _attributes.get(key, "")}
                            for key, value in parsed_attributes.items()
                        }

                        span["attributes"] = [
                            {"key": key, "value": value}
                            for key, value in parsed_attributes.items()
                        ]
                        if plugin_name == DATA_TRUNCATION_PLUGIN_NAMESPACE:
                            span["attributes"].extend(
                                [
                                    {
                                        "key": POSTMAN_DATA_TRUNCATION_ATTRIBUTE_NAME,
                                        "value": {"boolValue": True},
                                    }
                                ]
                            )
                        if plugin_name == DATA_REDACTION_PLUGIN_NAMESPACE:
                            span["attributes"].extend(
                                [
                                    {
                                        "key": POSTMAN_DATA_REDACTION_FLAG_ATTRIBUTE_NAME,
                                        "value": {"boolValue": True},
                                    }
                                ]
                            )
                except Exception as plugin_error:
                    spans[span_idx] = "plugin_failed"

                    _LOG.warning(
                        f"Failed to run {plugin_name} plugin, this span will be dropped."
                    )
                    _LOG.debug(f"Failed span is - {span}")
                    _LOG.error(plugin_error)
                    # Skip other plugins if one fails.
                    break
        return spans

    def _export(self, serialized_data: str):
        """
        :param serialized_data:
        :return:
        """

        if self.postman_tracer.is_suppressed():
            return EmptyResponse()

        # Note: Explore if Multi-process, multi-thread can cause
        # session conflicts ?
        self._session.headers.update(_OTL_JSON_CONTENT_HEADER)
        export_request = ExportTraceServiceRequest.FromString(serialized_data)
        json_data = MessageToDict(export_request)

        if self.plugins:
            scope_spans = json_data.get("resourceSpans", [{}])[0].get(
                "scopeSpans", [{}]
            )
            for scope_span in scope_spans:
                spans = scope_span.get("spans", [])
                if spans:
                    modified_spans = self.run_plugins(spans=spans)

                    modified_spans = list(
                        filter(lambda span: span != "plugin_failed", modified_spans)
                    )

                    scope_span["spans"] = modified_spans

        _LOG.debug(f"Postman SDK: Trace Service Data Exported: {json_data}")
        resp = self._session.post(
            url=self._endpoint,
            data=json.dumps(json_data),
            verify=self._certificate_file,
            timeout=self._timeout,
        )

        if resp.status_code:
            _LOG.debug(f"Postman SDK Trace Service Response {resp.status_code}")

        return resp
