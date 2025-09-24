# app/types/db_models.py

"""
Database models.
~Task model
~Category model
"""

from dataclasses import dataclass
from typing import List
from enum import Enum
from datetime import datetime

class TaskStatus(Enum):
    """ Task status """
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    DELETED = "deleted"

class TaskPriority(Enum):
    """ Task priority """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Occurrence(Enum):
    """ Occurrence """
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class CategoryColor(Enum):
    """ Category color """
    REDPURPLE = "#ff3860"
    BLUEVIOLET = "#3860ff"
    GREENYELLOW = "#ffff00"
    YELLOWGREEN = "#00ff00"
    ORANGE = "#ff7f00"
    PINK = "#ff00ff"
    

@dataclass
class Task:
    """ Task model """
    id : int
    task_id : str
    task_name : str
    task_description : str
    status : TaskStatus
    priority : TaskPriority
    occurrence : Occurrence
    due_date : str # dd/mm/yyyy
    created_at : datetime
    updated_at : datetime
    category_id : int

@dataclass
class Category:
    """ Category model """
    id : int
    category_id : str
    category_name : str
    category_color : CategoryColor
    created_at : datetime
    updated_at : datetime
