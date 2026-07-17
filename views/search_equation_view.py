"""
search_equation_view.py
Section 2 — Search Equation.
VSCode-style editor for building/refining the boolean search string,
with validate / load / save / run actions.
"""

import customtkinter as ctk
from styles.theme import Color, Font, Icon, Spacing
from components.card import Card, SectionLabel
from components.buttons import PrimaryButton, SecondaryButton, OutlineButton
from components.editor import CodeEditor
from tkinter import messagebox
from services.console_service import console
from services.app_state import state

SAMPLE_EQUATION = (
    '("machine learning" OR "deep learning") AND\n'
    '("cardiovascular disease" OR "heart disease") AND\n'
    '("early diagnosis" OR "risk prediction")\n'
    'NOT ("animal study")'
)


class SearchEquationView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Color.TRANSPARENT, **kwargs)
        self._build()
        state.subscribe(self.refresh)

    def _build(self):
        card = Card(
            self,
            title="Search Equation",
            subtitle="Write and validate the boolean query used to retrieve papers.",
            icon=Icon.EQUATION,
        )
        card.pack(
            fill="both",
            expand=True,
            padx=Spacing.XL,
            pady=Spacing.LG
        )

        body = card.body

        SectionLabel(body, text="Query Editor").pack(fill="x", pady=(0, 6))
        self.editor = CodeEditor(body, placeholder_text=SAMPLE_EQUATION, height=220)
        self.editor.pack(
            fill="x",
            pady=(0, Spacing.MD)
        )

        # Actions
        actions = ctk.CTkFrame(body, fg_color=Color.TRANSPARENT)
        actions.pack(fill="x")

        SecondaryButton(actions, text="Save", icon=Icon.SAVE, command=self.save_equation).pack(side="right", padx=(Spacing.SM, 0))

    def refresh(self):

        if state.equation == "":
            return

        self.editor.delete(
            "1.0",
            "end"
        )

        self.editor.insert_text(
            state.equation
        )

    def save_equation(self):    

        state.equation = self.editor.get_text().strip()

        console.success("Equation saved.")

        messagebox.showinfo(
            "SearchAI",
            "Equation saved."
        )