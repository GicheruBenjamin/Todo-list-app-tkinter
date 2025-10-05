# app/types/query.py

"""
Query Types
------------
Defines the structure for building SQLite-compatible queries with strong typing.
Supports:
- Nested logical filters (AND/OR)
- All standard comparison operators plus IS_NULL/IS_NOT_NULL
- Sorting, pagination, projection
- DISTINCT selection
- Future-proof for group_by / aggregates
"""

from typing import TypedDict, List, Union, Optional, Tuple
from enum import Enum


# === Enums ===

class FilterLogic(Enum):
    """Logical operators for combining filter groups."""
    AND = "AND"
    OR = "OR"


class FilterOperator(Enum):
    """Comparison operators for SQLite."""
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
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"


class SortOrder(Enum):
    """Sorting direction."""
    ASC = "asc"
    DESC = "desc"


# === TypedDicts ===

class FilterCondition(TypedDict, total=False):
    """
    Represents a single condition inside a filter group.
    - field: Column name
    - operator: FilterOperator
    - value: Value(s) for comparison (ignored for IS_NULL/IS_NOT_NULL)
    """
    field: str
    operator: FilterOperator
    value: Union[str, int, float, bool, List, Tuple]


class FilterGroup(TypedDict, total=False):
    """
    Group of filters combined with a logical operator.
    Can contain nested FilterGroup(s) or FilterCondition(s).
    """
    logic: FilterLogic
    conditions: List[Union["FilterGroup", FilterCondition]]


class SortSpec(TypedDict, total=False):
    """Sorting specification for one field."""
    field: str
    order: SortOrder


class PageSet(TypedDict, total=False):
    """Pagination settings."""
    page_no: int
    page_limit: int
    offset: int
    start: Optional[str]  # Optional for range queries
    finish: Optional[str]


class Projection(TypedDict, total=False):
    """
    Fields to include or exclude from SELECT.
    - include: only these fields
    - exclude: remove these fields from '*'
    """
    include: Optional[List[str]]
    exclude: Optional[List[str]]


class Query(TypedDict, total=False):
    """
    Full query definition compatible with SQLite.
    - filters: FilterGroup for WHERE clause
    - sorts: List of SortSpec
    - page_set: Pagination options
    - projection: Projection (include/exclude)
    - distinct: True if SELECT DISTINCT is needed
    - group_by: List of columns for GROUP BY (future use)
    """
    filters: Optional[FilterGroup]
    sorts: Optional[List[SortSpec]]
    page_set: Optional[PageSet]
    projection: Optional[Projection]
    distinct: Optional[bool]
    group_by: Optional[List[str]]
