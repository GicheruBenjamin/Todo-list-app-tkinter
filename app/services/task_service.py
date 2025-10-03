# app/services/task_service.py

"""
TaskService
-----------
Provides business logic operations for the Task model.
Handles creation, updates, deletion, retrieval, filtering,
and other task-specific operations through the Repo layer.
"""

from app.repo.repo import Repo
from app.types.db_models import Task, TaskStatus, TaskPriority, Occurrence
from app.utils.generate_entity_id import generate_entity_id, EntityType
from datetime import datetime

class TaskService:
    """
    Service class for managing Task entities.
    """

    def __init__(self, repo: Repo):
        """
        Initialize service with a Repo instance.
        """
        self.repo = repo

    # === Create task ===
    def create_task(self, name: str, description: str, priority: TaskPriority, occurrence: Occurrence, due_date: str, category_id: str | None = None) -> dict:
        """
        Create a new task with a generated ID.
        Returns the created task as a dict.
        """
        task_id = generate_entity_id(EntityType.TASK)
        item = {
            "task_id": task_id,
            "task_name": name,
            "task_description": description,
            "status": TaskStatus.ACTIVE.value,
            "priority": priority.value,
            "occurrence": occurrence.value,
            "due_date": due_date,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "category_id": category_id
        }
        self.repo.create_new_item(item)
        return item

    # === Update task ===
    def update_task(self, task_id: str, updates: dict) -> bool:
        """
        Update an existing task by ID.
        Returns True if successful.
        """
        updates["updated_at"] = datetime.now()
        return self.repo.update_item({"task_id": task_id}, updates)

    # === Delete task ===
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by ID.
        """
        return self.repo.delete_item({"task_id": task_id})

    # === Get task by ID ===
    def get_task(self, task_id: str) -> dict | None:
        """
        Retrieve a task by its ID.
        """
        query = {"filters": {"logic": "AND", "conditions": [{"field": "task_id", "operator": "eq", "value": task_id}]}}
        return self.repo.get_one(query)

    # === List tasks ===
    def list_tasks(self, filters: dict | None = None) -> list[dict]:
        """
        Retrieve all tasks matching optional filters.
        """
        query = filters or {}
        return self.repo.get_many(query)
