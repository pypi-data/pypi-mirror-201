"""
This module contains utility functions used in the Postman SDK.

"""
import json
from typing import Optional
from urllib.parse import urlparse

from postman_sdk.model.base_config import BaseConfig
from postman_sdk.receiver_service import (
    BOOTSTRAP_PATH,
    TRACE_RECEIVER_PATH,
    HEALTHCHECK_PATH,
)
from postman_sdk.util.logger import _LOG


def unpack_url(url: str):
    """
    This function takes a URL as input and returns a dictionary with two keys - "target" and "query". The "target"
    key contains the path of the URL, and the "query" key contains a JSON string with the query parameters of the URL.
    :param url: string
    :return dict
    """
    parsed_url = urlparse(url)

    return {"target": parsed_url.path, "query": parse_query_string(parsed_url.query)}


def parse_query_string(query: str) -> str:
    """
    Parses the Query string.
    :param query:
    """
    if isinstance(query, str) and query:
        query_items = query.split("&")
        query_obj = {}

        for qry in query_items:
            if "=" in qry:
                try:
                    key, val = qry.split("=")
                    query_obj[key] = val
                except:
                    _LOG.warning(f"Postman: url query parse error {qry}")

        return json.dumps(query_obj)

    return query


def add_postman_excluded_urls(config: BaseConfig):
    """
    This function returns a comma-separated string of URLs that should be excluded
    from tracing in the Postman SDK. The URLs that are excluded are the bootstrap path, trace receiver path,
    health check path, and any additional URLs specified in the Postman SDK configuration.

    **This is only applicable on outgoing requests / requests originating from the server.**
    :parm config;BaseConfig
    :return str.
    """
    excludes = [
        f"{config.receiver_base_url}{BOOTSTRAP_PATH}",
        f"{config.receiver_base_url}{TRACE_RECEIVER_PATH}",
        f"{config.receiver_base_url}{HEALTHCHECK_PATH}",
    ]

    if config.ignore_outgoing_requests:
        excludes.extend(config.ignore_outgoing_requests)

    return ",".join(excludes)


def add_user_excluded_urls(url_regexes: Optional[list]) -> Optional[str]:
    """
    This function returns a comma-separated string of URLs that should be excluded
    from tracing in the Postman SDK.

    It takes into account the user-defined exclusion list and returns a compatible version for
    downstream instrumentations.

    **This is only applicable on incoming requests to the server.**
    """
    if url_regexes:
        return ",".join(url_regexes)
