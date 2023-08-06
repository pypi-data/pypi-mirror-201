"""Defines the `ParameterValue` class, used by the `Case` and `Run` classes.
"""
from typing import TypedDict

# parameter value type
class ParameterValue(TypedDict):
    """A name-value pair of parameter values.
    """
    id: str
    value: float

__all__ = ["ParameterValue"]