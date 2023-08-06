"""
Data truncation module
"""
import json
from json import JSONDecodeError

from opentelemetry.util.types import Attributes

from postman_sdk.util.constants import (
    DEFAULT_TRUNCATION_MAX_DEPTH,
    TRUNCATION_START_LEVEL,
)


# pylint: disable=import-outside-toplevel


class DataTruncation:
    """
    DataTruncation plugin, plugin reshapes the json payload with <key>:<type>. level will define how deeps this should
    apply.
    """

    level: int

    def __init__(self, max_depth=DEFAULT_TRUNCATION_MAX_DEPTH):
        """
        Constructor
        :param level:
        """
        self.max_depth = max_depth

    def run(self, span_attributes: Attributes):
        """
        entry point to run the redaction.
        :param span_attributes:
        :return: span_attributes
        """

        from postman_sdk.plugins import (
            SPAN_HTTP_BODY_ATTRIBUTES_NAMES,
            POSTMAN_DATA_TRUNCATION_ATTRIBUTE_NAME,
        )

        for _, span_attrib_name in SPAN_HTTP_BODY_ATTRIBUTES_NAMES.items():
            data = span_attributes.get(span_attrib_name)

            if data:
                truncated_data = self._truncate_data(data)
                span_attributes[span_attrib_name] = truncated_data

        span_attributes[POSTMAN_DATA_TRUNCATION_ATTRIBUTE_NAME] = True

        return span_attributes

    def _truncate_data(self, data, current_level=TRUNCATION_START_LEVEL):
        """
        :param data:
        :param current_level:
        :return:
        """
        string_data_input = False

        if not data:
            return data

        if isinstance(data, str):
            string_data_input = True

            try:
                data = json.loads(data)
            except JSONDecodeError:
                return data

        if not isinstance(data, dict) and not isinstance(data, list):
            return {"type": type(data).__name__}

        # We can have list or dict by this part so, will use enumerate to help iterate.
        # enumerate results in index and item in case of list and index of a key, key in case of dict
        for idx, dat_key in enumerate(data):
            dat_val = data[dat_key] if isinstance(data, dict) else data[idx]
            data_type = {"type": type(dat_val).__name__}

            if isinstance(dat_val, dict) or isinstance(dat_val, list):
                if current_level <= self.max_depth:
                    data_type = self._truncate_data(
                        data=dat_val, current_level=current_level + 1
                    )
                elif not dat_val:
                    if isinstance(dat_val, dict):
                        data[dat_key] = data_type
                    else:
                        data[idx] = data_type
                else:
                    if isinstance(data, dict):
                        data[dat_key] = {"type": type(dat_val).__name__}
                    else:
                        data[idx] = data_type

            if isinstance(data, dict):
                data[dat_key] = data_type
            else:
                data[idx] = data_type

        if string_data_input:
            data = json.dumps(data)

        return data
