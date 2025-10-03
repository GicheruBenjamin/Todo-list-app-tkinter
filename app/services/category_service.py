# app/services/category_service.py

"""
CategoryService
---------------
Provides business logic operations for the Category model.
Handles creation, update, deletion, retrieval, and validation 
of categories through the Repo abstraction layer.
"""

from app.repo.repo import Repo
from app.types.db_models import Category, CategoryColor
from app.utils.generate_entity_id import generate_entity_id, EntityType
from datetime import datetime

class CategoryService:
    """
    Service class for managing Category entities.
    """

    def __init__(self, repo: Repo):
        """
        Initialize service with a Repo instance.
        """
        self.repo = repo

    # === Create category ===
    def create_category(self, name: str, color: CategoryColor) -> dict:
        """
        Create a new category with a generated ID.
        Returns the created category as a dict.
        """
        category_id = generate_entity_id(EntityType.CATEGORY)
        item = {
            "category_id": category_id,
            "category_name": name,
            "category_color": color.value,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        self.repo.create_new_item(item)
        return item

    # === Update category ===
    def update_category(self, category_id: str, updates: dict) -> bool:
        """
        Update an existing category by ID.
        Returns True if successful, False otherwise.
        """
        updates["updated_at"] = datetime.now()
        return self.repo.update_item({"category_id": category_id}, updates)

    # === Delete category ===
    def delete_category(self, category_id: str) -> bool:
        """
        Delete a category by ID.
        """
        return self.repo.delete_item({"category_id": category_id})

    # === Get category by ID ===
    def get_category(self, category_id: str) -> dict | None:
        """
        Retrieve a category by its ID.
        """
        query = {"filters": {"logic": "AND", "conditions": [{"field": "category_id", "operator": "eq", "value": category_id}]}}
        return self.repo.get_one(query)

    # === List categories ===
    def list_categories(self) -> list[dict]:
        """
        Retrieve all categories.
        """
        query = {}
        return self.repo.get_many(query)
