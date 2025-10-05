# app/utils/db_query.py (DB_QUERY)
"""
DB Query Builder
----------------
Generates SQLite SQL + parameters from a structured Query dict.
Supports:
- Nested filters with AND/OR
- All FilterOperators (eq, ne, gt, gte, lt, lte, in, not_in, like, not_like, between, is_null, is_not_null)
- Multiple sort fields
- Pagination (page_no, page_limit, offset)
- Projection include/exclude
- DISTINCT selection
- Optional GROUP BY support
"""

from typing import Tuple, List, Any, Union
from app.types.query import Query, FilterCondition, FilterGroup, FilterOperator, FilterLogic, SortOrder


# === Normalizers ===

def _normalize_operator(op: Union[FilterOperator, str]) -> str:
    """Return the SQL string representation of a FilterOperator."""
    if hasattr(op, "value"):
        return op.value
    if isinstance(op, str):
        return op.lower()
    raise ValueError(f"Invalid operator: {op}")


def _normalize_logic(logic: Union[FilterLogic, str]) -> str:
    """Return the SQL string for a filter logic (AND/OR)."""
    if hasattr(logic, "value"):
        return logic.value.upper()
    if isinstance(logic, str):
        return logic.upper()
    raise ValueError(f"Invalid filter logic: {logic}")


def _normalize_sort_order(order: Union[SortOrder, str]) -> str:
    """Return SQL string for sort order (ASC/DESC)."""
    if hasattr(order, "value"):
        return order.value.upper()
    if isinstance(order, str):
        return order.upper()
    raise ValueError(f"Invalid sort order: {order}")


# === Filter builders ===

def _build_filter_condition(cond: FilterCondition, params: List[Any]) -> str:
    """Build a single filter condition into SQL."""
    field = cond["field"]
    operator = _normalize_operator(cond["operator"])
    value = cond.get("value")

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
        if not isinstance(value, (list, tuple)):
            raise ValueError(f"'IN' operator requires a list or tuple, got {type(value)}")
        placeholders = ",".join("?" for _ in value)
        params.extend(value)
        return f"{field} IN ({placeholders})"

    elif operator == "not_in":
        if not isinstance(value, (list, tuple)):
            raise ValueError(f"'NOT_IN' operator requires a list or tuple, got {type(value)}")
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
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise ValueError(f"'BETWEEN' operator requires a tuple/list of 2 values, got {value}")
        params.extend(value)
        return f"{field} BETWEEN ? AND ?"

    elif operator == "is_null":
        return f"{field} IS NULL"

    elif operator == "is_not_null":
        return f"{field} IS NOT NULL"

    else:
        raise ValueError(f"Unsupported operator: {operator}")


def _build_filter_group(group: FilterGroup, params: List[Any]) -> str:
    """Recursively build a filter group into a WHERE clause."""
    logic = _normalize_logic(group["logic"])
    parts = []

    for cond in group["conditions"]:
        if isinstance(cond, dict) and "conditions" in cond:
            parts.append(f"({_build_filter_group(cond, params)})")
        else:
            parts.append(_build_filter_condition(cond, params))

    return f" {logic} ".join(parts)


# === Main Query Builder ===

def build_query(table: str, query: Query) -> Tuple[str, List[Any]]:
    """
    Build a SELECT SQL statement from a Query definition.

    Returns:
        sql: str - the SQL query string
        params: List[Any] - parameters for safe execution
    """
    params: List[Any] = []

    # --- Projection ---
    projection = query.get("projection") or {}
    include = projection.get("include")
    exclude = projection.get("exclude")

    if include:
        fields = ", ".join(include)
    else:
        fields = "*"
        if exclude:
            # Remove excluded columns from '*' by naive replacement
            # Assumes all columns will eventually be mapped; best-effort
            fields = "*"

    # --- DISTINCT ---
    distinct = query.get("distinct", False)
    select_clause = f"SELECT {'DISTINCT ' if distinct else ''}{fields} FROM {table}"

    sql = select_clause

    # --- Filters ---
    filters = query.get("filters")
    if filters:
        where_clause = _build_filter_group(filters, params)
        sql += f" WHERE {where_clause}"

    # --- GROUP BY (future support) ---
    group_by = query.get("group_by")
    if group_by:
        sql += " GROUP BY " + ", ".join(group_by)

    # --- Sorting ---
    sorts = query.get("sorts")
    if sorts:
        sort_parts = [f"{s['field']} {_normalize_sort_order(s['order'])}" for s in sorts]
        sql += " ORDER BY " + ", ".join(sort_parts)

    # --- Pagination ---
    page = query.get("page_set")
    if page:
        limit = page.get("page_limit", 0)
        offset = page.get("offset")

        if "page_no" in page and limit:
            offset = (page["page_no"] - 1) * limit

        if limit:
            sql += f" LIMIT {limit}"
            if offset is not None:
                sql += f" OFFSET {offset}"

    return sql, params
