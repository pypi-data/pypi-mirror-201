"""
module for data redaction models.
"""
# pylint:disable=E0611,R0903
from typing import Dict, Optional

from pydantic import BaseModel

from postman_sdk.model.dynamic_model import DynamicBaseModel


class Rules(DynamicBaseModel):
    """
    Rules object
    """

    __root__: Dict[str, str]


class DataRedactionConfig(BaseModel):
    """
    DataRedaction config model.
    """

    enable: bool = True
    rules: Optional[Rules]
