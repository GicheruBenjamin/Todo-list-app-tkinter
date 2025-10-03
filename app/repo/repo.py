# app/repo/repo.py

"""
Repo abstraction layer for SQLite database operations.
-------------------------------------------------------
This class provides a unified interface for CRUD and query 
operations, abstracting away direct SQL interaction.

Supported operations:
1. create_new_item(item: dict)
2. update_item(identity: dict[str, Any], updates: dict[str, Any])
3. delete_item(identity: dict[str, Any])
4. get_one(query: dict)
5. get_many(query: dict)
6. get_count(query: dict)
7. check_if_exists(query: dict)
"""

from typing import Any, Optional, List
from app.types import DatabaseConnection, Query
from app.utils import build_query


class Repo:
    """
    Repository class that abstracts database operations
    over a given SQLite connection.
    """

    def __init__(self, db: DatabaseConnection, table: str):
        """
        Initialize repository with database connection and target table.
        """
        self.db = db
        self.table = table

    # === Create ===
    def create_new_item(self, item: dict) -> bool:
        """
        Insert a new item into the table.
        ~ item: dict of field:value
        ~ return: bool (success/failure)
        """
        try:
            placeholders = ", ".join("?" for _ in item)
            columns = ", ".join(item.keys())
            sql = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
            self.db.execute(sql, tuple(item.values()))
            self.db.commit()
            return True
        except Exception:
            return False

    # === Update ===
    def update_item(self, identity: dict[str, Any], updates: dict[str, Any]) -> bool:
        """
        Update an existing item based on identity filter.
        ~ identity: dict to locate row(s)
        ~ updates: dict of fields to update
        """
        try:
            set_clause = ", ".join(f"{k}=?" for k in updates.keys())
            where_clause = " AND ".join(f"{k}=?" for k in identity.keys())
            sql = f"UPDATE {self.table} SET {set_clause} WHERE {where_clause}"
            params = list(updates.values()) + list(identity.values())
            self.db.execute(sql, params)
            self.db.commit()
            return True
        except Exception:
            return False

    # === Delete ===
    def delete_item(self, identity: dict[str, Any]) -> bool:
        """
        Delete an item based on identity filter.
        ~ identity: dict to locate row(s)
        """
        try:
            where_clause = " AND ".join(f"{k}=?" for k in identity.keys())
            sql = f"DELETE FROM {self.table} WHERE {where_clause}"
            self.db.execute(sql, tuple(identity.values()))
            self.db.commit()
            return True
        except Exception:
            return False

    # === Get one ===
    def get_one(self, query: Query) -> Optional[dict]:
        """
        Fetch a single row matching query.
        ~ query: Query definition dict
        ~ return: dict or None
        """
        sql, params = build_query(self.table, query)
        cursor = self.db.execute(sql + " LIMIT 1", params)
        row = cursor.fetchone()
        return dict(row) if row else None

    # === Get many ===
    def get_many(self, query: Query) -> List[dict]:
        """
        Fetch multiple rows matching query.
        ~ query: Query definition dict
        ~ return: list of dicts
        """
        sql, params = build_query(self.table, query)
        cursor = self.db.execute(sql, params)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]

    # === Count ===
    def get_count(self, query: Query) -> int:
        """
        Count rows matching query.
        ~ query: Query definition dict
        ~ return: int count
        """
        sql, params = build_query(self.table, query)
        count_sql = f"SELECT COUNT(*) FROM ({sql})"
        cursor = self.db.execute(count_sql, params)
        return cursor.fetchone()[0]

    # === Existence check ===
    def check_if_exists(self, query: Query) -> bool:
        """
        Check if at least one row matches query.
        ~ query: Query definition dict
        ~ return: bool
        """
        sql, params = build_query(self.table, query)
        cursor = self.db.execute(sql + " LIMIT 1", params)
        return cursor.fetchone() is not None
