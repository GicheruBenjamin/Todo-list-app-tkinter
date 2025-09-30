# app/repo/repo.py

"""
Class Repo:
     Abstraction for database operations.
     1. create_new_item(item: dict)
     2. update_item(identity: dict[str, any], updates: dict[str, any])
     3. delete_item(identity: dict[str, any])
     4. get_one(query:dict)
     5. get_many(query:dict)
     6. get_count(query:dict)
     7. check_if_exists(query:dict)
"""
from app.types import DatabaseConnection

