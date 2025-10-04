# app/components/main_component.py

"""
Main Component
--------------
Combines Task and Category components into one application window.
Acts as the entry point for the UI.
"""

import tkinter as tk
from app.components.task_component import TaskComponent
from app.components.category_component import CategoryComponent

class MainComponent(tk.Tk):
    """
    The main application window, holding task and category views.
    """
    def __init__(self, task_service, category_service):
        super().__init__()
        self.title("Task & Category Manager")
        self.geometry("600x400")

        self.task_frame = TaskComponent(self, task_service)
        self.task_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.category_frame = CategoryComponent(self, category_service)
        self.category_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)


