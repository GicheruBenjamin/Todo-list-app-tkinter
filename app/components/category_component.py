"""
CategoryComponent
-----------------
Tkinter UI component to manage categories.
Allows creating, updating, deleting, and listing categories
using CategoryService.
"""

import tkinter as tk
from tkinter import messagebox
from app.services.category_service import CategoryService, CategoryColor

class CategoryComponent(tk.Frame):
    """
    UI frame for displaying and managing categories.
    """
    def __init__(self, parent, category_service: CategoryService):
        super().__init__(parent)
        self.category_service = category_service
        self.pack(fill="both", expand=True)

        # ---------------- UI ELEMENTS ----------------
        self.listbox = tk.Listbox(self)
        self.listbox.pack(side="left", fill="both", expand=True)

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(side="right", fill="y")

        self.add_btn = tk.Button(self.btn_frame, text="Add Category", command=self.add_category)
        self.add_btn.pack(pady=5)

        self.update_btn = tk.Button(self.btn_frame, text="Update Selected", command=self.update_category)
        self.update_btn.pack(pady=5)

        self.delete_btn = tk.Button(self.btn_frame, text="Delete Selected", command=self.delete_category)
        self.delete_btn.pack(pady=5)

        self.refresh_categories()

    # ----------------- FUNCTIONS -----------------
    def refresh_categories(self):
        """Load all categories into the listbox."""
        self.listbox.delete(0, tk.END)
        self.categories = self.category_service.list_categories() or []
        for cat in self.categories:
            self.listbox.insert(tk.END, f"{cat['category_name']} ({cat['category_color']})")

    def add_category(self):
        """Prompt to add a new category."""
        name = tk.simpledialog.askstring("Category Name", "Enter category name:")
        if not name:
            return
        color = CategoryColor.BLUEVIOLET  # Default for demo
        success = self.category_service.create_category(name, color)
        if success:
            messagebox.showinfo("Success", f"Category '{name}' added!")
            self.refresh_categories()

    def update_category(self):
        """Update the selected category."""
        idx = self.listbox.curselection()
        if not idx:
            return
        cat = self.categories[idx[0]]
        new_name = tk.simpledialog.askstring("Update Name", "Enter new name:", initialvalue=cat["category_name"])
        if not new_name:
            return
        self.category_service.update_category(cat["category_id"], {"category_name": new_name})
        self.refresh_categories()

    def delete_category(self):
        """Delete the selected category."""
        idx = self.listbox.curselection()
        if not idx:
            return
        cat = self.categories[idx[0]]
        if messagebox.askyesno("Confirm", f"Delete category '{cat['category_name']}'?"):
            self.category_service.delete_category(cat["category_id"])
            self.refresh_categories()
