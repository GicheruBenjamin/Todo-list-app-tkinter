"""
Main UI entry point.
-------------------
Initializes the Tkinter window and plugs in the category and task components
with their respective services.
"""

import tkinter as tk
from app.db.init_sqlite import init_sqlite, close_sqlite
from app.config import provide_app_config
from app.repo import init_repos
from app.services.category_service import CategoryService
from app.services.task_service import TaskService
from app.components import CategoryComponent, TaskComponent
import logging

logging.basicConfig(level=logging.INFO)

def main():
    # ---------------- App Config & DB ----------------
    app_config = provide_app_config()
    connection = init_sqlite(app_config.db_settings)

    repos = init_repos(connection)
    category_service = CategoryService(repos)
    task_service = TaskService(repos)

    # ---------------- Tkinter Window ----------------
    root = tk.Tk()
    root.title(app_config.app_info.window_title)
    root.geometry(f"{app_config.app_info.window_size[0]}x{app_config.app_info.window_size[1]}")

    # ---------------- Components ----------------
    category_frame = CategoryComponent(root, category_service)
    category_frame.pack(side="left", fill="both", expand=True)

    task_frame = TaskComponent(root, task_service)
    task_frame.pack(side="right", fill="both", expand=True)

    # ---------------- Run App ----------------
    root.mainloop()
    close_sqlite(connection)

if __name__ == "__main__":
    main()
