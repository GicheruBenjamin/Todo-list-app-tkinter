"""
TaskService
-----------
Provides business logic operations for the Task model.
Handles creation, update, deletion, retrieval, and validation 
of tasks through the Repo abstraction layer.
"""

from datetime import datetime
from typing import Optional, List
from app.types.db_models import Task, TaskStatus, TaskPriority, Occurrence
from app.utils.generate_entity_id import generate_entity_id, EntityType


class TaskService:
    """
    Business logic layer for Task operations.
    Uses a Repo instance to perform CRUD operations.
    """

    def __init__(self, repo):
        """
        Initialize TaskService with a Repos container.

        Args:
            repo: Repos container with task repo instance
        """
        self.repo = repo
        self.task_repo = repo.task

    # ----------------- CREATE TASK -----------------
    def create_task(
        self,
        task_name: str,
        task_description: str,
        status: TaskStatus = TaskStatus.ACTIVE,
        priority: TaskPriority = TaskPriority.MEDIUM,
        occurrence: Occurrence = Occurrence.DAILY,
        due_date: str = "",
        category_id: Optional[str] = None
    ) -> bool:
        """
        Create a new task with a generated task_id.

        Returns True if creation succeeds.
        """
        task_data = {
            "task_id": generate_entity_id(EntityType.TASK),
            "task_name": task_name,
            "task_description": task_description,
            "status": status.value,
            "priority": priority.value,
            "occurrence": occurrence.value,
            "due_date": due_date,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "category_id": category_id,
        }
        return self.task_repo.create_new_item(task_data)

    # ----------------- UPDATE TASK -----------------
    def update_task(self, task_id: str, updates: dict) -> bool:
        """
        Update a task by its task_id.
        """
        return self.task_repo.update_item({"task_id": task_id}, updates)

    # ----------------- DELETE TASK -----------------
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by its task_id.
        """
        return self.task_repo.delete_item({"task_id": task_id})

    # ----------------- GET TASK -----------------
    def get_task(self, task_id: str) -> Optional[dict]:
        """
        Retrieve a single task by task_id.
        """
        query = {"filters": {"logic": "AND", "conditions": [{"field": "task_id", "operator": "eq", "value": task_id}]}}
        return self.task_repo.get_one(query)

    # ----------------- LIST TASKS -----------------
    def list_tasks(self, query: dict = None) -> List[dict]:
        """
        Retrieve multiple tasks optionally filtered by a query.
        """
        return self.task_repo.get_many(query or {})

    # ----------------- COUNT TASKS -----------------
    def count_tasks(self, query: dict = None) -> int:
        """
        Count tasks optionally filtered by a query.
        """
        return self.task_repo.get_count(query or {})

    # ----------------- CHECK EXISTENCE -----------------
    def task_exists(self, task_id: str) -> bool:
        """
        Check if a task with given task_id exists.
        """
        query = {"filters": {"logic": "AND", "conditions": [{"field": "task_id", "operator": "eq", "value": task_id}]}}
        return self.task_repo.check_if_exists(query)
