"""
TaskCard Component
------------------
Displays a single task with Edit and Delete actions.
"""

import tkinter as tk
from tkinter import ttk


class TaskCard(tk.Frame):
    """UI element representing one task."""

    def __init__(self, parent, task_data, on_edit, on_delete):
        super().__init__(parent, relief="ridge", borderwidth=2, padx=5, pady=5)
        self.task_data = task_data

        ttk.Label(self, text=f"{task_data['task_name']} ({task_data['priority']})",
                  font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(self, text=f"{task_data['task_description']}", wraplength=250).grid(row=1, column=0, sticky="w")

        ttk.Button(self, text="Edit", command=lambda: on_edit(task_data)).grid(row=2, column=0, pady=5, sticky="w")
        ttk.Button(self, text="Delete", command=lambda: on_delete(task_data)).grid(row=2, column=1, pady=5)
