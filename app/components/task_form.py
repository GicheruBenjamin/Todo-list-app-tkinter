"""
TaskForm Component
------------------
Tkinter form for creating or updating a task.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from app.types.db_models import TaskPriority, Occurrence


class TaskForm(tk.Frame):
    """Form for adding or editing tasks."""

    def __init__(self, parent, task_service, category_service, refresh_callback=None, edit_data=None):
        super().__init__(parent, padx=10, pady=10)
        self.task_service = task_service
        self.category_service = category_service
        self.refresh_callback = refresh_callback
        self.edit_data = edit_data

        # --- State ---
        self.task_name = tk.StringVar()
        self.task_description = tk.StringVar()
        self.priority = tk.StringVar(value=TaskPriority.MEDIUM.value)
        self.occurrence = tk.StringVar(value=Occurrence.DAILY.value)
        self.category_id = tk.StringVar()

        # --- Load Categories ---
        self.categories = [c["category_id"] for c in self.category_service.list_categories()]

        # --- Form Layout ---
        ttk.Label(self, text="Task Name:").grid(row=0, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.task_name, width=30).grid(row=0, column=1, pady=5)

        ttk.Label(self, text="Description:").grid(row=1, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.task_description, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(self, text="Priority:").grid(row=2, column=0, sticky="w")
        ttk.OptionMenu(self, self.priority, self.priority.get(),
                       *[p.value for p in TaskPriority]).grid(row=2, column=1, pady=5)

        ttk.Label(self, text="Occurrence:").grid(row=3, column=0, sticky="w")
        ttk.OptionMenu(self, self.occurrence, self.occurrence.get(),
                       *[o.value for o in Occurrence]).grid(row=3, column=1, pady=5)

        ttk.Label(self, text="Category:").grid(row=4, column=0, sticky="w")
        ttk.OptionMenu(self, self.category_id,
                       self.categories[0] if self.categories else "",
                       *self.categories).grid(row=4, column=1, pady=5)

        ttk.Button(self, text="Save", command=self._on_save).grid(row=5, column=0, pady=10)
        ttk.Button(self, text="Cancel", command=self._clear_form).grid(row=5, column=1, pady=10)

    def _on_save(self):
        """Save or update a task."""
        name = self.task_name.get().strip()
        desc = self.task_description.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Task name cannot be empty.")
            return

        try:
            if self.edit_data:
                self.task_service.update_task(self.edit_data["task_id"], {
                    "task_name": name,
                    "task_description": desc,
                    "priority": self.priority.get(),
                    "occurrence": self.occurrence.get(),
                    "category_id": self.category_id.get()
                })
            else:
                self.task_service.create_task(
                    name, desc, self.priority.get(), self.occurrence.get(), self.category_id.get()
                )

            messagebox.showinfo("Success", "Task saved successfully.")
            if self.refresh_callback:
                self.refresh_callback()
            self._clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _clear_form(self):
        """Clear the form."""
        self.task_name.set("")
        self.task_description.set("")
