# app/repo/__init__.py (REPO)
"""
Repo Package
------------
Provides centralized repository objects for the application.
Each repo handles CRUD operations for a specific table.

Includes:
- RepoType: type alias for Repo
- Repos: dataclass holding all repos
- init_repos: function to initialize all repos with a DB connection
"""

from dataclasses import dataclass
from typing import Type
from app.types import DatabaseConnection
from .repo import Repo

# Type alias for a Repo class
RepoType = Type[Repo]

@dataclass
class Repos:
    """
    Container for all repository instances used in the application.
    """
    task: RepoType
    category: RepoType


def init_repos(connection: DatabaseConnection) -> Repos:
    """
    Initialize repository objects with a SQLite database connection.
    
    Args:
        connection (DatabaseConnection): Active SQLite connection
    
    Returns:
        Repos: dataclass containing initialized Repo instances
    """
    return Repos(
        task=Repo(connection, "task"),
        category=Repo(connection, "category"),
    )

__all__ = [
    "Repos",
    "init_repos",
]