"""
Main Application Entry Point
----------------------------
Initializes database, services, and UI components.
"""

from app.db.init_sqlite import init_sqlite
from app.config import provide_app_config
from app.repo import init_repos

def main():
    """Start the application."""
    # Load config & DB
    config = provide_app_config()
    connection = init_sqlite(config.db_settings)
    repos = init_repos(connection)
    print(f" Repo: {repos}")
    print("App started.")


if __name__ == "__main__":
    main()
