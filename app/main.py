"""
Main entry point for testing TaskService and CategoryService.
Initializes SQLite, repositories, and services, then runs
CRUD operations to validate functionality.
"""

import logging
from datetime import datetime
from app.db.init_sqlite import init_sqlite, close_sqlite
from app.config import provide_app_config
from app.repo import init_repos
from app.services.task_service import TaskService
from app.services.category_service import CategoryService
from app.types.db_models import CategoryColor

logging.basicConfig(level=logging.INFO)

def main():
    # -------------------- Load App Config --------------------
    app_config = provide_app_config()
    db_settings = app_config.db_settings

    # -------------------- Initialize SQLite --------------------
    connection = init_sqlite(db_settings)
    if not connection:
        logging.error("Failed to initialize DB")
        return

    # -------------------- Initialize Repos --------------------
    repos = init_repos(connection)

    # -------------------- Initialize Services --------------------
    category_service = CategoryService(repos)
    task_service = TaskService(repos)

    # -------------------- TEST CATEGORY CRUD --------------------
    logging.info("=== CATEGORY CRUD TESTS ===")
    category_service.create_category("Work", CategoryColor.BLUEVIOLET)
    category_service.create_category("Personal", CategoryColor.GREENYELLOW)

    categories = category_service.list_categories()
    logging.info(f"All Categories: {categories}")

    first_category_id = categories[0]["category_id"]
    category_service.update_category(first_category_id, {"category_name": "Work Updated"})
    logging.info(f"Updated Category: {category_service.get_category(first_category_id)}")

    exists = category_service.category_exists(first_category_id)
    logging.info(f"Category exists: {exists}")

    count = category_service.count_categories()
    logging.info(f"Total categories count: {count}")

    # -------------------- TEST TASK CRUD --------------------
    logging.info("=== TASK CRUD TESTS ===")
    task_service.create_task(
        "Finish report", 
        "Complete the financial report", 
        category_id=first_category_id
    )

    task_service.create_task(
        "Buy groceries", 
        "Milk, Bread, Eggs"
    )

    tasks = task_service.list_tasks()
    logging.info(f"All Tasks: {tasks}")

    first_task_id = tasks[0]["task_id"]
    task_service.update_task(first_task_id, {"task_name": "Finish report ASAP"})
    logging.info(f"Updated Task: {task_service.get_task(first_task_id)}")

    exists = task_service.task_exists(first_task_id)
    logging.info(f"Task exists: {exists}")

    count = task_service.count_tasks()
    logging.info(f"Total tasks count: {count}")

    # -------------------- CLEANUP --------------------
    close_sqlite(connection)
    logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
