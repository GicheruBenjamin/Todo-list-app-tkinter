# app/repo/repo.py (REPO)
"""
Repo Abstraction Layer for SQLite Database Operations
-----------------------------------------------------
This class provides a unified interface for CRUD and query operations,
abstracting away direct SQL interaction.

Supported operations:
1. create_new_item(item: dict) -> bool
2. update_item(identity: dict[str, Any], updates: dict[str, Any]) -> bool
3. delete_item(identity: dict[str, Any]) -> bool
4. get_one(query: Query) -> Optional[dict]
5. get_many(query: Query) -> List[dict]
6. get_count(query: Query) -> Optional[int]
7. check_if_exists(query: Query) -> bool
"""

from typing import Any, List, Optional, Dict
from app.types import DatabaseConnection, Query
from app.utils.build_query import build_query


class Repo:
    """CRUD operations for a single table in the SQLite database."""

    def __init__(self, connection: DatabaseConnection, table: str):
        """
        Initialize the repository with a DB connection and table name.
        """
        self.connection = connection
        self.table = table

    # ----------------- CREATE -----------------
    def create_new_item(self, item: dict) -> bool:
        """
        Insert a new row into the table.
        Returns True on success.
        """
        try:
            columns = ", ".join(item.keys())
            placeholders = ", ".join("?" for _ in item)
            sql = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
            with self.connection:
                self.connection.execute(sql, tuple(item.values()))
            return True
        except Exception as e:
            print("Insert failed:", e)
            return False

    # ----------------- UPDATE -----------------
    def update_item(self, identity: dict[str, Any], updates: dict[str, Any]) -> bool:
        """
        Update rows matching identity with the provided updates.
        Returns True on success.
        """
        try:
            set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
            where_clause = " AND ".join(f"{k} = ?" for k in identity.keys())
            sql = f"UPDATE {self.table} SET {set_clause} WHERE {where_clause}"
            with self.connection:
                self.connection.execute(sql, tuple(updates.values()) + tuple(identity.values()))
            return True
        except Exception as e:
            print("Update failed:", e)
            return False

    # ----------------- DELETE -----------------
    def delete_item(self, identity: dict[str, Any]) -> bool:
        """
        Delete rows matching identity.
        Returns True on success.
        """
        try:
            where_clause = " AND ".join(f"{k} = ?" for k in identity.keys())
            sql = f"DELETE FROM {self.table} WHERE {where_clause}"
            with self.connection:
                self.connection.execute(sql, tuple(identity.values()))
            return True
        except Exception as e:
            print("Delete failed:", e)
            return False

    # ----------------- GET ONE -----------------
    def get_one(self, query: Query) -> Optional[Dict]:
        """
        Return a single row matching the query as a dict.
        Returns None if no row found.
        """
        try:
            sql, params = build_query(self.table, query)
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            row = cursor.fetchone()
            if row is None:
                return None
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        except Exception as e:
            print("Get one failed:", e)
            return None
        finally:
            cursor.close()

    # ----------------- GET MANY -----------------
    def get_many(self, query: Query) -> List[Dict]:
        """
        Return all rows matching the query as a list of dicts.
        """
        try:
            sql, params = build_query(self.table, query)
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print("Get many failed:", e)
            return []
        finally:
            cursor.close()

    # ----------------- GET COUNT -----------------
    def get_count(self, query: Query) -> Optional[int]:
        """
        Return the number of rows matching the query.
        """
        try:
            sql, params = build_query(self.table, query)
            count_sql = f"SELECT COUNT(*) FROM ({sql})"
            cursor = self.connection.cursor()
            cursor.execute(count_sql, params)
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            print("Get count failed:", e)
            return None
        finally:
            cursor.close()

    # ----------------- CHECK IF EXISTS -----------------
    def check_if_exists(self, query: Query) -> bool:
        """
        Return True if any row matches the query, else False.
        """
        try:
            sql, params = build_query(self.table, query)
            exists_sql = f"SELECT 1 FROM ({sql}) LIMIT 1"
            cursor = self.connection.cursor()
            cursor.execute(exists_sql, params)
            return bool(cursor.fetchone())
        except Exception as e:
            print("Check exists failed:", e)
            return False
        finally:
            cursor.close()
