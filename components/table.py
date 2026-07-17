"""
table.py
Reusable dark-themed table component built on ttk.Treeview, used for the
articles list (AI Analysis) and the iteration history log.
"""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from styles.theme import Color, Font, Radius, Spacing


class DataTable(ctk.CTkFrame):
    """
    A styled Treeview wrapped in a CTkFrame.
    `columns` is a list of (key, label, width) tuples.
    `rows` is a list of dicts keyed by column key (sample/static data only).
    """

    def __init__(self, master, columns, rows=None, height=18, **kwargs):
        super().__init__(
            master,
            fg_color=Color.BG_CARD,
            corner_radius=Radius.MD,
            border_width=1,
            border_color=Color.BORDER_SOFT,
            **kwargs,
        )

        self._configure_style()

        col_keys = [c[0] for c in columns]
        self.tree = ttk.Treeview(
            self,
            columns=col_keys,
            show="headings",
            style="SearchAI.Treeview",
            height=height,
        )

        for key, label, width in columns:
            self.tree.heading(key, text=label, anchor="w")
            self.tree.column(key, width=width, anchor="w", stretch=True)

        scrollbar = ctk.CTkScrollbar(self, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(Spacing.SM, 0), pady=Spacing.SM)
        scrollbar.pack(side="right", fill="y", padx=(0, Spacing.SM), pady=Spacing.SM)

        if rows:
            self.load_rows(columns, rows)

    def selected_row(self):
        selection = self.tree.selection()

        if not selection:
            return None

        return self.tree.item(selection[0])["values"]

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "SearchAI.Treeview",
            background=Color.BG_CARD,
            foreground=Color.TEXT_PRIMARY,
            fieldbackground=Color.BG_CARD,
            borderwidth=0,
            rowheight=42,
            font=("Segoe UI", 12),
        )
        style.configure(
            "SearchAI.Treeview.Heading",
            background=Color.BG_SIDEBAR,
            foreground=Color.TEXT_MUTED,
            borderwidth=0,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
        )
        style.map(
            "SearchAI.Treeview",
            background=[("selected", Color.PRIMARY)],
            foreground=[("selected", Color.TEXT_PRIMARY)],
        )
        style.map("SearchAI.Treeview.Heading", background=[("active", Color.BG_SIDEBAR)])
        style.layout("SearchAI.Treeview", [
            ("SearchAI.Treeview.treearea", {"sticky": "nswe"})
        ])

    def load_rows(self, columns, rows):
        """Populate the table with a list of dicts (static demo data)."""
        self.tree.delete(*self.tree.get_children())
        col_keys = [c[0] for c in columns]
        for row in rows:
            values = [row.get(k, "") for k in col_keys]
            self.tree.insert("", "end", values=values)

    def clear(self):
        self.tree.delete(*self.tree.get_children())
