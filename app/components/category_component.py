# app/components/category_component.py

"""
Category Component
------------------
Provides UI for creating, listing, and deleting categories.
Uses CategoryService to persist data.
"""

import tkinter as tk
from tkinter import messagebox
from app.services.category_service import CategoryService

class CategoryComponent(tk.Frame):
    """
    A frame that displays categories and allows adding/deleting them.
    """
    def __init__(self, parent, category_service: CategoryService):
        super().__init__(parent)
        self.category_service = category_service
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        """Build UI elements: entry, add button, listbox, delete button."""
        self.entry = tk.Entry(self)
        self.entry.pack(pady=5)

        self.add_btn = tk.Button(self, text="Add Category", command=self.add_category)
        self.add_btn.pack(pady=5)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, pady=5)

        self.delete_btn = tk.Button(self, text="Delete Selected", command=self.delete_category)
        self.delete_btn.pack(pady=5)

        self.refresh()

    def add_category(self):
        """Add a category via service and refresh the list."""
        name = self.entry.get()
        if not name:
            messagebox.showwarning("Validation", "Category name required")
            return
        self.category_service.create_category({"category_name": name, "category_color": "#3860ff"})
        self.entry.delete(0, tk.END)
        self.refresh()

    def delete_category(self):
        """Delete the selected category."""
        try:
            selection = self.listbox.curselection()[0]
            category = self.listbox.get(selection)
            self.category_service.delete_category({"category_name": category})
            self.refresh()
        except IndexError:
            messagebox.showwarning("Validation", "Select a category to delete")

    def refresh(self):
        """Refresh the category listbox."""
        self.listbox.delete(0, tk.END)
        cats = self.category_service.get_categories({})
        for c in cats:
            self.listbox.insert(tk.END, c["category_name"])
