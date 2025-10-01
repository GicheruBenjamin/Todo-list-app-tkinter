# app/utils/db_query.py
"""
DB Query Builder
----------------
Takes a Query dict (see app/types/query.py) and generates
SQLite SQL + parameter list.

Supports:
- Nested filters with AND/OR
- All FilterOperators (eq, ne, gt, gte, lt, lte, in, not_in, like, not_like, between)
- Multiple sort fields
- Pagination (page_no, limit, offset)
- Projection (include/exclude)
"""

from typing import Tuple, List, Any, Union
from app.types import (
    Query,
    FilterCondition,
    FilterGroup,
    FilterOperator,
    FilterLogic,
    SortOrder,
)


# === Normalizers ===

def _normalize_operator(op: Union[FilterOperator, str]) -> str:
    if hasattr(op, "value"):  # Enum
        return op.value
    if isinstance(op, str):
        return op.lower()
    raise ValueError(f"Invalid operator: {op}")


def _normalize_logic(logic: Union[FilterLogic, str]) -> str:
    if hasattr(logic, "value"):  # Enum
        return logic.value
    if isinstance(logic, str):
        return logic.upper()
    raise ValueError(f"Invalid filter logic: {logic}")


def _normalize_sort_order(order: Union[SortOrder, str]) -> str:
    if hasattr(order, "value"):  # Enum
        return order.value.upper()
    if isinstance(order, str):
        return order.upper()
    raise ValueError(f"Invalid sort order: {order}")


# === Filter builders ===

def _build_filter_condition(cond: FilterCondition, params: List[Any]) -> str:
    """Build a single filter condition into SQL."""
    field = cond["field"]
    operator = _normalize_operator(cond["operator"])
    value = cond["value"]

    if operator == "eq":
        params.append(value)
        return f"{field} = ?"

    elif operator == "ne":
        params.append(value)
        return f"{field} != ?"

    elif operator == "gt":
        params.append(value)
        return f"{field} > ?"

    elif operator == "gte":
        params.append(value)
        return f"{field} >= ?"

    elif operator == "lt":
        params.append(value)
        return f"{field} < ?"

    elif operator == "lte":
        params.append(value)
        return f"{field} <= ?"

    elif operator == "in":
        placeholders = ",".join("?" for _ in value)
        params.extend(value)
        return f"{field} IN ({placeholders})"

    elif operator == "not_in":
        placeholders = ",".join("?" for _ in value)
        params.extend(value)
        return f"{field} NOT IN ({placeholders})"

    elif operator == "like":
        params.append(value)
        return f"{field} LIKE ?"

    elif operator == "not_like":
        params.append(value)
        return f"{field} NOT LIKE ?"

    elif operator == "between":
        start, end = value
        params.extend([start, end])
        return f"{field} BETWEEN ? AND ?"

    else:
        raise ValueError(f"Unsupported operator: {operator}")


def _build_filter_group(group: FilterGroup, params: List[Any]) -> str:
    """Recursively build a filter group into SQL."""
    logic = _normalize_logic(group["logic"])
    parts = []

    for cond in group["conditions"]:
        if isinstance(cond, dict) and "conditions" in cond:  # nested group
            parts.append(f"({_build_filter_group(cond, params)})")
        else:
            parts.append(_build_filter_condition(cond, params))

    return f" {logic} ".join(parts)


# === Main query builder ===

def build_query(table: str, query: Query) -> Tuple[str, List[Any]]:
    """
    Build a SELECT SQL statement from a Query definition.
    Returns: (sql, params)
    """
    params: List[Any] = []

    # --- Projection ---
    projection = query.get("projection", {})
    include = projection.get("include")
    exclude = projection.get("exclude")

    if include:
        fields = ", ".join(include)
    else:
        fields = "*"
    sql = f"SELECT {fields} FROM {table}"

    # --- Filters ---
    if "filters" in query:
        where_clause = _build_filter_group(query["filters"], params)
        sql += f" WHERE {where_clause}"

    # --- Sorting ---
    if "sorts" in query:
        sort_parts = [
            f"{s['field']} {_normalize_sort_order(s['order'])}"
            for s in query["sorts"]
        ]
        sql += " ORDER BY " + ", ".join(sort_parts)

    # --- Pagination ---
    if "page_set" in query:
        page = query["page_set"]
        limit = page.get("page_limit", 0)
        offset = page.get("offset")

        if "page_no" in page and limit:
            offset = (page["page_no"] - 1) * limit

        if limit:
            sql += f" LIMIT {limit}"
            if offset is not None:
                sql += f" OFFSET {offset}"

    return sql, params
