"""
Main Application Entry Point
----------------------------
Initializes database, services, and UI components.
"""

from app.db.init_sqlite import init_sqlite
from app.config import provide_app_config
from app.repo.repo import Repo
from app.services.task_service import TaskService
from app.services.category_service import CategoryService
from app.components import MainComponent

def main():
    """Start the application."""
    # Load config & DB
    config = provide_app_config()
    connection = init_sqlite(config.db_settings)

    # Init repos
    repo = Repo(connection, "tasks")

    # Init services
    task_service = TaskService(repo)
    category_service = CategoryService(repo)

    # Launch UI
    app = MainComponent(task_service, category_service)
    app.mainloop()

if __name__ == "__main__":
    main()
