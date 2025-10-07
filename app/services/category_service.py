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
