"""
TaskComponent
-------------
Tkinter UI component to manage tasks.
Allows creating, updating, deleting, and listing tasks using TaskService.
"""

import tkinter as tk
from tkinter import messagebox
from app.services.task_service import TaskService

class TaskComponent(tk.Frame):
    """
    UI frame for displaying and managing tasks.
    """
    def __init__(self, parent, task_service: TaskService):
        super().__init__(parent)
        self.task_service = task_service
        self.pack(fill="both", expand=True)

        # ---------------- UI ELEMENTS ----------------
        self.listbox = tk.Listbox(self)
        self.listbox.pack(side="left", fill="both", expand=True)

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(side="right", fill="y")

        self.add_btn = tk.Button(self.btn_frame, text="Add Task", command=self.add_task)
        self.add_btn.pack(pady=5)

        self.update_btn = tk.Button(self.btn_frame, text="Update Selected", command=self.update_task)
        self.update_btn.pack(pady=5)

        self.delete_btn = tk.Button(self.btn_frame, text="Delete Selected", command=self.delete_task)
        self.delete_btn.pack(pady=5)

        self.refresh_tasks()

    # ----------------- FUNCTIONS -----------------
    def refresh_tasks(self):
        """Load all tasks into the listbox."""
        self.listbox.delete(0, tk.END)
        self.tasks = self.task_service.list_tasks() or []
        for t in self.tasks:
            self.listbox.insert(tk.END, f"{t['task_name']} (Due: {t['due_date']})")

    def add_task(self):
        """Prompt to add a new task."""
        name = tk.simpledialog.askstring("Task Name", "Enter task name:")
        if not name:
            return
        description = tk.simpledialog.askstring("Description", "Enter description:")
        self.task_service.create_task(name, description)
        self.refresh_tasks()

    def update_task(self):
        """Update the selected task."""
        idx = self.listbox.curselection()
        if not idx:
            return
        task = self.tasks[idx[0]]
        new_name = tk.simpledialog.askstring("Update Name", "Enter new task name:", initialvalue=task["task_name"])
        if not new_name:
            return
        self.task_service.update_task(task["task_id"], {"task_name": new_name})
        self.refresh_tasks()

    def delete_task(self):
        """Delete the selected task."""
        idx = self.listbox.curselection()
        if not idx:
            return
        task = self.tasks[idx[0]]
        if messagebox.askyesno("Confirm", f"Delete task '{task['task_name']}'?"):
            self.task_service.delete_task(task["task_id"])
            self.refresh_tasks()
