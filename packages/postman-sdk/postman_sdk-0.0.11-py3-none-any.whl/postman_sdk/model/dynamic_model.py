"""
Custom Model supporting dynamic fields.
"""
# pylint:disable=E0611
from typing import Dict

from pydantic import BaseModel


class DynamicBaseModel(BaseModel):
    """
    Pydantic custom model for dynamic fields support
    """

    def get_keys(self):
        """
        Get all the key names
        :return:
        """
        if hasattr(self, "__root__") and isinstance(self.__root__, Dict):
            return self.__root__.keys()

        return None

    def get_items(self):
        """
        Get iter of fields, values
        :return:
        """
        if hasattr(self, "__root__") and isinstance(self.__root__, Dict):
            return self.__root__.items()

        return None

    def get_entries(self):
        """
        Get list items if dynamic fields are list.
        :return:
        """
        if hasattr(self, "__root__") and isinstance(self.__root__, list):
            return self.__root__

        return None

    def get(self, key):
        """
        Check if the field name exists and return value if found.
        :param key:
        :return:
        """
        if hasattr(self, "__root__") and isinstance(self.__root__, Dict):
            return self.__root__.get(key)

        return None
