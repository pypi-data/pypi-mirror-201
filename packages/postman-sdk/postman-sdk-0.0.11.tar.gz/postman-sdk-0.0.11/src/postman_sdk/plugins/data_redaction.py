"""
Data redaction module, will apply redaction on the values of attribute keys by the given reg rules.
"""
import json
import re
from json.decoder import JSONDecodeError

from opentelemetry.util.types import Attributes

from postman_sdk.model.data_redaction import (
    DataRedactionConfig,
)
from postman_sdk.util.logger import _LOG

# pylint: disable=W0212,W0612,import-outside-toplevel


class DataRedactor:
    """
    DataRedactor, must be loaded with Span exporter and invoke at end_span hook.
    """

    regex_redaction = {}

    def __init__(self, redaction_rules: DataRedactionConfig):
        self.__compile_rules(redaction_rules.rules)

    def __compile_rules(self, rules):
        """
        Method to parse rules and index
        :param rules:
        :return:
        """
        # Preventing circular import.
        from postman_sdk.plugins import DEFAULT_REDACTION_RULES

        combined_rules = {}

        if hasattr(rules, "__root__"):
            # In case of conflict, the items from rules will override the DEFAULT_REDACTION_RULES.
            combined_rules.update(rules.__root__)

        combined_rules.update(DEFAULT_REDACTION_RULES)
        # Making sure that user rules are given priority.

        for rl_name, regex_rule_compiled in combined_rules.items():
            self.regex_redaction[rl_name] = re.compile(
                regex_rule_compiled, re.IGNORECASE
            )

    def run(self, span_attributes: Attributes):
        """
        Method to run the redaction.
        :param span_attributes:
        :return: span_attributes
        """
        redacted_result_by_section = {}

        for req_type in ["request", "response"]:
            span_attributes, redacted_result = self.__redact(span_attributes, req_type)

            if redacted_result:
                redacted_result_by_section[req_type] = redacted_result

        if redacted_result_by_section:
            from postman_sdk.plugins import POSTMAN_DATA_REDACTION_FLAG_ATTRIBUTE_NAME

            span_attributes[POSTMAN_DATA_REDACTION_FLAG_ATTRIBUTE_NAME] = True
            # TO-DO capture what rules applied
            # span_attributes[POSTMAN_REDACTED_ATTRIBUTE_NAME] = json.dumps(redacted_result_by_section)

        return span_attributes

    def __redact(self, span_attributes, req_type):
        """
        Method to run redaction.
        :param span_attributes:
        :param req_type:
        :return:
        """
        redact_engine_map = {}

        if req_type == "request":
            from postman_sdk.plugins import HTTP_ATTRIBUTES__REQUEST_REDACTION_MAP

            redact_engine_map = HTTP_ATTRIBUTES__REQUEST_REDACTION_MAP
        elif req_type == "response":
            from postman_sdk.plugins import HTTP_ATTRIBUTES__RESPONSE_REDACTION_MAP

            redact_engine_map = HTTP_ATTRIBUTES__RESPONSE_REDACTION_MAP
        else:
            _LOG.warning("Unknown redaction request section")

            return span_attributes
        rules_applied = {}
        for section, engine_map in redact_engine_map.items():
            attribute = engine_map["attribute_key"]
            data = span_attributes.get(attribute)

            if not data:
                _LOG.debug(
                    f"No data for {attribute} for {req_type} section of the request, no"
                    " redaction applied"
                )

                continue

            _LOG.debug(f"Processing redaction {section} section on {req_type} ")

            redaction_method = engine_map["redaction_function"]

            for reg_ex_label, reg_rl in self.regex_redaction.items():
                replaced = getattr(self, redaction_method)(data, reg_rl)

                if data == replaced:
                    continue

                redacted_attributes = rules_applied.setdefault(attribute, [])

                if reg_ex_label not in redacted_attributes:
                    redacted_attributes.append(reg_ex_label)

                span_attributes[attribute] = replaced
                data = replaced

        return span_attributes, rules_applied

    @staticmethod
    def __obfuscate_json_string(json_string: str, regex_compiled):
        """
        RApply given reg ex rule on the value of the json pared object and return stringified json.
        :param regex_compiled:
        :param json_string:
        :return:
        """
        from postman_sdk.plugins import DEFAULT_REDACTION_REPLACEMENT_STRING

        try:
            json_obj = json.loads(json_string)
        except JSONDecodeError:
            _LOG.warning(f"Unable to decode incoming JSON string: {json_string}")

            return json_string

        if isinstance(json_obj, dict):
            for key_name, val in json_obj.items():
                data_val = val if isinstance(val, str) else json.dumps(val)
                data_val = regex_compiled.sub(
                    DEFAULT_REDACTION_REPLACEMENT_STRING, data_val
                )

                json_obj[key_name] = data_val
        elif isinstance(json_obj, list):
            for idx, item in enumerate(json_obj):
                data_val = item if isinstance(item, str) else json.dumps(item)

                json_obj[idx] = DataRedactor.__obfuscate_string(
                    data_val, regex_compiled
                )

        return json.dumps(json_obj)

    @staticmethod
    def __obfuscate_string(text_content, regex_compiled):
        """
        Apply given rex ex on the input string and return results.
        :param regex_compiled:
        :param text_content:
        :return:
        """
        from postman_sdk.plugins import DEFAULT_REDACTION_REPLACEMENT_STRING

        return regex_compiled.sub(DEFAULT_REDACTION_REPLACEMENT_STRING, text_content)

    @staticmethod
    def redact_headers_data(data, reg_ex_compiled):
        """
        Method to call redaction on  headers
        :param reg_ex_compiled:
        :param data:
        :return:
        """
        if not reg_ex_compiled or not data:
            return data

        return DataRedactor.__obfuscate_json_string(data, reg_ex_compiled)

    @staticmethod
    def redact_body_data(data, reg_ex_compiled):
        """
        Method to call redaction on Body
        :param reg_ex_compiled:
        :param data:
        :return:
        """
        if not reg_ex_compiled or not data:
            return data

        return DataRedactor.__obfuscate_string(data, reg_ex_compiled)

    @staticmethod
    def redact_query_data(data, reg_ex_compiled):
        """
        method to call redaction on parsed Query in dict format
        :param data:
        :param reg_ex_compiled:
        :return:
        """
        if not reg_ex_compiled or not data:
            return data

        return DataRedactor.__obfuscate_json_string(data, reg_ex_compiled)

    @staticmethod
    def redact_uristring_data(data, reg_ex_compiled):
        """
        Method to call redaction on string forma of query params.
        :param data:
        :param reg_ex_compiled:
        :return:
        """
        if not reg_ex_compiled or not data:
            return data

        return DataRedactor.__obfuscate_string(data, reg_ex_compiled)
