# app/services/__init__.py

"""
Services package for business logic.
------------------------------------
Contains service classes that provide high-level operations 
on domain models (Category, Task) using the Repo layer.

Modules:
- category_service.py
- task_service.py
"""

from .category_service import CategoryService
from .task_service import TaskService

__all__ = [
    "CategoryService",
    "TaskService",
]
