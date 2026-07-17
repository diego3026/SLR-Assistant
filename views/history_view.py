"""
history_view.py
Section 6 — Iteration History.
Log of previous search iterations with the ability to restore an equation.
"""

import customtkinter as ctk
from styles.theme import Color, Font, Icon, Spacing
from components.card import Card, SectionLabel
from components.table import DataTable
from components.buttons import SecondaryButton
from services.app_state import state

COLUMNS = [
    ("iteration","Iteration",90),
    ("equation","Equation",430),
    ("total","Articles",90),
    ("high","High",80),
    ("relevant","Relevant",90),
    ("date","Date",120)
]

class HistoryView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Color.TRANSPARENT, **kwargs)
        self._build()
        state.subscribe(self.refresh)

    def _build(self):
        card = Card(
            self,
            title="Iteration History",
            subtitle="Track how your search equation evolved across iterations.",
            icon=Icon.HISTORY,
        )
        card.pack(fill="both", expand=True, padx=Spacing.XL, pady=Spacing.LG)

        body = card.body

        SectionLabel(body, text="Previous Iterations").pack(fill="x", pady=(0, 8))
        self.table = DataTable(
            body,
            COLUMNS,
            [],
        )

        self.table.pack(
            fill="both",
            pady=(0, Spacing.MD)
        )

        actions = ctk.CTkFrame(body, fg_color=Color.TRANSPARENT)
        actions.pack(fill="x")
        ctk.CTkLabel(
            actions, text="Select a row to restore its equation.",
            font=Font.small(), text_color=Color.TEXT_MUTED
        ).pack(side="left")
        SecondaryButton(
            actions,
            text="Restore",
            icon=Icon.RESTORE,
            command=self.restore
        ).pack(side="right")

    def restore(self):
        row = self.table.selected_row()
        if row is None:
            return

        equation = row[1]
        state.equation = equation
        state.notify()

    def refresh(self):
        rows = []
        for item in state.history:
            rows.append(
                {
                    "iteration": item["iteration"],
                    "equation": item["equation"],
                    "relevant": item["relevant"],
                    "date": item["date"]
                }
            )

        self.table.load_rows(
            COLUMNS,
            rows
        )