"""
Enum for http verbs.
"""
from enum import Enum


class HTTPVerbEnum(str, Enum):
    """
    Http verbs enum
    """

    POST = "POST"
    GET = "GET"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    PUT = "PUT"

    @staticmethod
    def to_string():
        """
        enum class to string
        :return:
        """
        return ",".join([en for en in HTTPVerbEnum])


class EmptyResponse:
    """
    Util class to mock span export response.
    """

    def __init__(self, status_code=200, data=dict()) -> None:
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data
