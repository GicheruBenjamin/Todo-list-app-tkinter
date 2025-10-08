"""
CategoryForm Component
----------------------
Tkinter form for creating or updating a category.
Handles input, validation, and submission through CategoryService.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from app.types.db_models import CategoryColor


class CategoryForm(tk.Frame):
    """UI form for creating or editing categories."""

    def __init__(self, parent, category_service, refresh_callback=None, edit_data=None):
        super().__init__(parent, padx=10, pady=10)
        self.category_service = category_service
        self.refresh_callback = refresh_callback
        self.edit_data = edit_data

        # --- State ---
        self.category_name = tk.StringVar()
        self.category_color = tk.StringVar(value=list(CategoryColor)[0].value)

        if edit_data:
            self.category_name.set(edit_data.get("category_name", ""))
            self.category_color.set(edit_data.get("category_color", ""))

        # --- Layout ---
        ttk.Label(self, text="Name:").grid(row=0, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.category_name, width=30).grid(row=0, column=1, pady=5)

        ttk.Label(self, text="Color:").grid(row=1, column=0, sticky="w")
        color_menu = ttk.OptionMenu(self, self.category_color, self.category_color.get(),
                                    *[c.value for c in CategoryColor])
        color_menu.grid(row=1, column=1, pady=5)

        # --- Actions ---
        ttk.Button(self, text="Save", command=self._on_save).grid(row=2, column=0, pady=10)
        ttk.Button(self, text="Cancel", command=self._clear_form).grid(row=2, column=1, pady=10)

    def _on_save(self):
        """Handle save or update."""
        name = self.category_name.get().strip()
        color = self.category_color.get().strip()

        if not name:
            messagebox.showwarning("Missing name", "Category name cannot be empty.")
            return

        try:
            if self.edit_data:
                self.category_service.update_category(self.edit_data["category_id"], {
                    "category_name": name, "category_color": color
                })
            else:
                self.category_service.create_category(name, CategoryColor(color))

            messagebox.showinfo("Success", "Category saved successfully.")
            if self.refresh_callback:
                self.refresh_callback()
            self._clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _clear_form(self):
        """Reset the form."""
        self.category_name.set("")
        self.category_color.set(list(CategoryColor)[0].value)
