"""
CategoryList Component
----------------------
Displays a list of CategoryCard components.
Handles dynamic refresh from CategoryService.
"""

import tkinter as tk
from app.components.category_card import CategoryCard


class CategoryList(tk.Frame):
    """Scrollable container for category cards."""

    def __init__(self, parent, category_service, on_edit):
        super().__init__(parent, padx=10, pady=10)
        self.category_service = category_service
        self.on_edit = on_edit
        self.cards = []

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
        """Refresh category list display."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        categories = self.category_service.list_categories()
        for c in categories:
            card = CategoryCard(self.scroll_frame, c, self.on_edit, self._on_delete)
            card.pack(fill="x", pady=5)
            self.cards.append(card)

    def _on_delete(self, category_data):
        """Handle category deletion."""
        self.category_service.delete_category(category_data["category_id"])
        self.refresh()
