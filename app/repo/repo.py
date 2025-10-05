# app/repo/repo.py

"""
Repo abstraction layer for SQLite database operations.
-------------------------------------------------------
This class provides a unified interface for CRUD and query 
operations, abstracting away direct SQL interaction.

Supported operations:
1. create_new_item(item: dict) -> bool
   onsuccess = True
   onfailure = False
2. update_item(identity: dict[str, Any], updates: dict[str, Any]) -> bool
   onsuccess = True
   onfailure = False
3. delete_item(identity: dict[str, Any]) -> bool
   onsuccess = True
   onfailure = False
4. get_one(query: dict) -> dict | None
   onsuccess = dict
   onfailure = None
5. get_many(query: dict) -> list[dict] | None
   onsuccess = list
   onfailure = None
6. get_count(query: dict) -> int | None
   onsuccess = int
   onfailure = None
7. check_if_exists(query: dict) -> bool | None
   onsuccess = bool True if exists False if not
   onfailure = None
"""

from app.types import DatabaseConnection, Query
from app.utils import build_query