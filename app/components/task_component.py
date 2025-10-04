# app/components/task_component.py

"""
Task Component
--------------
Provides UI for creating, listing, and deleting tasks.
Uses TaskService to persist data.
"""

import tkinter as tk
from tkinter import messagebox
from app.services.task_service import TaskService

class TaskComponent(tk.Frame):
    """
    A frame that displays tasks and allows adding/deleting them.
    """
    def __init__(self, parent, task_service: TaskService):
        super().__init__(parent)
        self.task_service = task_service
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        """Build UI elements: entry, add button, listbox, delete button."""
        self.entry = tk.Entry(self)
        self.entry.pack(pady=5)

        self.add_btn = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_btn.pack(pady=5)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, pady=5)

        self.delete_btn = tk.Button(self, text="Delete Selected", command=self.delete_task)
        self.delete_btn.pack(pady=5)

        self.refresh()

    def add_task(self):
        """Add a task via service and refresh the list."""
        name = self.entry.get()
        if not name:
            messagebox.showwarning("Validation", "Task name required")
            return
        self.task_service.create_task({
            "task_name": name,
            "task_description": "N/A",
            "status": "active",
            "priority": "medium",
            "occurrence": "daily",
            "due_date": "2025-12-31",
        })
        self.entry.delete(0, tk.END)
        self.refresh()

    def delete_task(self):
        """Delete the selected task."""
        try:
            selection = self.listbox.curselection()[0]
            task = self.listbox.get(selection)
            self.task_service.delete_task({"task_name": task})
            self.refresh()
        except IndexError:
            messagebox.showwarning("Validation", "Select a task to delete")

    def refresh(self):
        """Refresh the task listbox."""
        self.listbox.delete(0, tk.END)
        tasks = self.task_service.get_tasks({})
        for t in tasks:
            self.listbox.insert(tk.END, t["task_name"])
