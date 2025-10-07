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
from dataclasses import dataclass
from typing import Type
from app.repo import Repos

# TYpe CategoryService
CategoryServiceType = Type[CategoryService]
# Type TaskService
TaskServiceType = Type[TaskService]

@dataclass
class Services:
    """
    Container for all service instances used in the application.
    """
    category: CategoryServiceType
    task: TaskServiceType


def init_services(repos: Repos) -> Services:
    """
    Initialize service objects with a Repos container.
    
    Args:
        repos (Repos): Repos container with initialized repos
    
    Returns:
        Services: dataclass containing initialized service instances
    """
    return Services(
        category=CategoryService(repos),
        task=TaskService(repos),
    )
