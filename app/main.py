"""
Main Application Entry
----------------------
Integrates components and services into a working Tkinter UI.
"""

import tkinter as tk
from app.config import provide_app_config
from app.db.init_sqlite import init_sqlite
from app.repo import init_repos
from app.services import init_services
from app.components.category_form import CategoryForm
from app.components.category_list import CategoryList
from app.components.task_form import TaskForm
from app.components.task_list import TaskList


def main():
    config = provide_app_config()
    conn = init_sqlite(config.db_settings)
    repos = init_repos(conn)
    services = init_services(repos)

    root = tk.Tk()
    root.title(config.app_info.window_title)
    root.geometry("1000x600")

    # --- LAYOUT ---
    left_frame = tk.Frame(root)
    right_frame = tk.Frame(root)
    left_frame.pack(side="left", fill="both", expand=True)
    right_frame.pack(side="right", fill="both", expand=True)

    # --- CATEGORIES ---
    cat_list = CategoryList(left_frame, services.category, on_edit=lambda c: None)
    cat_list.pack(fill="both", expand=True)
    cat_form = CategoryForm(left_frame, services.category, refresh_callback=cat_list.refresh)
    cat_form.pack(fill="x")

    # --- TASKS ---
    task_list = TaskList(right_frame, services.task, on_edit=lambda t: None)
    task_list.pack(fill="both", expand=True)
    task_form = TaskForm(right_frame, services.task, services.category, refresh_callback=task_list.refresh)
    task_form.pack(fill="x")

    root.mainloop()


if __name__ == "__main__":
    main()
