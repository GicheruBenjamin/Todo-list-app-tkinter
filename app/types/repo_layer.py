# app/types/repo_layer.py
"""
Query types.
Defines the structure for filters, sorts, pagination, and projections.
"""

from typing import TypedDict, List, Union, Optional, Tuple
from enum import Enum


# === Enums ===

class FilterLogic(Enum):
    """Logical operators for combining filter groups."""
    AND = "AND"
    OR = "OR"


class FilterOperator(Enum):
    """Comparison operators."""
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NOT_IN = "not_in"
    LIKE = "like"
    NOT_LIKE = "not_like"
    BETWEEN = "between"


class SortOrder(Enum):
    """Sorting direction."""
    ASC = "asc"
    DESC = "desc"


# === Typed dicts ===

class FilterCondition(TypedDict):
    """A single condition inside a filter group."""
    field: str
    operator: FilterOperator
    value: Union[str, int, float, bool, List, Tuple]


class FilterGroup(TypedDict):
    """Group of filter conditions (can be nested)."""
    logic: FilterLogic
    conditions: List[Union["FilterGroup", FilterCondition]]


class SortSpec(TypedDict):
    """Sorting specification for one field."""
    field: str
    order: SortOrder


class PageSet(TypedDict, total=False):
    """Pagination settings."""
    page_no: int
    page_limit: int
    offset: int
    start: Optional[str]
    finish: Optional[str]


class Projection(TypedDict, total=False):
    """Fields to include/exclude from SELECT."""
    include: Optional[List[str]]
    exclude: Optional[List[str]]


class Query(TypedDict, total=False):
    """Full query definition."""
    filters: FilterGroup
    sorts: List[SortSpec]
    page_set: PageSet
    projection: Projection
