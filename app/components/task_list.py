"""
TaskList Component
------------------
Displays tasks in scrollable list with edit/delete options.
"""

import tkinter as tk
from app.components.task_card import TaskCard


class TaskList(tk.Frame):
    """Scrollable list for tasks."""

    def __init__(self, parent, task_service, on_edit):
        super().__init__(parent, padx=10, pady=10)
        self.task_service = task_service
        self.on_edit = on_edit

        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas)

        self.scroll_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.refresh()

    def refresh(self):
        """Refresh tasks."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        for t in self.task_service.list_tasks():
            TaskCard(self.scroll_frame, t, self.on_edit, self._on_delete).pack(fill="x", pady=5)

    def _on_delete(self, task):
        self.task_service.delete_task(task["task_id"])
        self.refresh()
