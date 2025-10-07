# app/components/__init__.py
"""
Components package.
------------------
Contains Tkinter UI components for the application.
"""

from .category_component import CategoryComponent
from .task_component import TaskComponent

__all__ = [
    "CategoryComponent",
    "TaskComponent",
]