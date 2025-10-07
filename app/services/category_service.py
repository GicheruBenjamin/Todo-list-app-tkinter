"""
CategoryService
---------------
Provides business logic operations for the Category model.
Handles creation, update, deletion, retrieval, and validation 
of categories through the Repo abstraction layer.
"""

from datetime import datetime
from typing import Optional, List
from app.types.db_models import Category, CategoryColor
from app.utils.generate_entity_id import generate_entity_id, EntityType


class CategoryService:
    """
    Business logic layer for Category operations.
    Uses a Repo instance to perform CRUD operations.
    """

    def __init__(self, repo):
        """
        Initialize CategoryService with a Repos container.

        Args:
            repo: Repos container with category repo instance
        """
        self.repo = repo
        self.cat_repo = repo.category

    # ----------------- CREATE CATEGORY -----------------
    def create_category(
        self, 
        category_name: str, 
        category_color: CategoryColor
    ) -> bool:
        """
        Create a new category with a generated category_id.
        """
        category_data = {
            "category_id": generate_entity_id(EntityType.CATEGORY),
            "category_name": category_name,
            "category_color": category_color.value,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        return self.cat_repo.create_new_item(category_data)

    # ----------------- UPDATE CATEGORY -----------------
    def update_category(self, category_id: str, updates: dict) -> bool:
        """
        Update a category by its category_id.
        """
        return self.cat_repo.update_item({"category_id": category_id}, updates)

    # ----------------- DELETE CATEGORY -----------------
    def delete_category(self, category_id: str) -> bool:
        """
        Delete a category by its category_id.
        """
        return self.cat_repo.delete_item({"category_id": category_id})

    # ----------------- GET CATEGORY -----------------
    def get_category(self, category_id: str) -> Optional[dict]:
        """
        Retrieve a single category by category_id.
        """
        query = {"filters": {"logic": "AND", "conditions": [{"field": "category_id", "operator": "eq", "value": category_id}]}}
        return self.cat_repo.get_one(query)

    # ----------------- LIST CATEGORIES -----------------
    def list_categories(self, query: dict = None) -> List[dict]:
        """
        Retrieve multiple categories optionally filtered by a query.
        """
        return self.cat_repo.get_many(query or {})

    # ----------------- COUNT CATEGORIES -----------------
    def count_categories(self, query: dict = None) -> int:
        """
        Count categories optionally filtered by a query.
        """
        return self.cat_repo.get_count(query or {})

    # ----------------- CHECK EXISTENCE -----------------
    def category_exists(self, category_id: str) -> bool:
        """
        Check if a category with given category_id exists.
        """
        query = {"filters": {"logic": "AND", "conditions": [{"field": "category_id", "operator": "eq", "value": category_id}]}}
        return self.cat_repo.check_if_exists(query)
