"""
CategoryCard Component
----------------------
Displays a single category with Edit and Delete buttons.
"""

import tkinter as tk
from tkinter import ttk


class CategoryCard(tk.Frame):
    """Displays category info and provides edit/delete options."""

    def __init__(self, parent, category_data, on_edit, on_delete):
        super().__init__(parent, relief="groove", borderwidth=2, padx=5, pady=5)
        self.category_data = category_data
        self.on_edit = on_edit
        self.on_delete = on_delete

        # --- Content ---
        ttk.Label(self, text=f"Name: {category_data['category_name']}",
                  font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(self, text=f"Color: {category_data['category_color']}",
                  background=category_data['category_color'], width=10).grid(row=0, column=1, padx=10)

        # --- Buttons ---
        ttk.Button(self, text="Edit", command=lambda: on_edit(category_data)).grid(row=1, column=0, pady=5)
        ttk.Button(self, text="Delete", command=lambda: on_delete(category_data)).grid(row=1, column=1, pady=5)
