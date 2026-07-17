"""
recommendations_view.py
Section 5 — Recommendations.
AI-suggested refinements to the search equation (add/remove terms, change
operators, add synonyms) plus a preview of the resulting equation.
"""

import customtkinter as ctk
from styles.theme import Color, Font, Icon, Spacing, Radius
from components.card import Card, SectionLabel
from components.buttons import PrimaryButton, OutlineButton
from components.editor import CodeEditor
from services.app_state import state

class RecommendationRow(ctk.CTkFrame):
    """One suggestion card with an icon tag, description and a small badge."""

    def __init__(self, master, icon, accent, tag, description, **kwargs):
        super().__init__(
            master, fg_color=Color.BG_INPUT, corner_radius=Radius.MD,
            border_width=1, border_color=Color.BORDER, **kwargs
        )
        inner = ctk.CTkFrame(self, fg_color=Color.TRANSPARENT)
        inner.pack(fill="x", padx=Spacing.MD, pady=Spacing.SM)

        self.icon_badge = ctk.CTkLabel(
            inner, text=icon, font=Font.h3(), text_color=accent, width=28
        )
        self.icon_badge.pack(side="left", padx=(0, Spacing.SM))

        text_col = ctk.CTkFrame(inner, fg_color=Color.TRANSPARENT)
        text_col.pack(side="left", fill="x", expand=True)

        self.tag_label = ctk.CTkLabel(
            text_col,
            text=tag.upper() if tag else "",
            font=Font.small(),
            text_color=accent,
            anchor="w"
        )
        self.tag_label.pack(fill="x")
        self.description_label = ctk.CTkLabel(
            text_col, text=description, font=Font.body(), text_color=Color.TEXT_PRIMARY,
            anchor="w", justify="left", wraplength=760
        )
        self.description_label.pack(fill="x", pady=(2, 0))

    def update(self, icon, accent, tag, description):

        self.icon_badge.configure(
            text=icon,
            text_color=accent
        )

        self.tag_label.configure(
            text=tag.upper() if tag else "",
            text_color=accent
        )

        self.description_label.configure(
            text=description
        )

class RecommendationsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Color.TRANSPARENT, **kwargs)
        self._build()
        state.subscribe(self.refresh)

    def _build(self):
        card = Card(
            self,
            title="Recommendations",
            subtitle="AI-generated suggestions to improve your search equation.",
            icon=Icon.RECOMMEND,
        )
        card.pack(fill="both", expand=True, padx=Spacing.XL, pady=Spacing.LG)

        body = card.body
        
        # =========================
        # Suggested Equation Preview
        # =========================

        SectionLabel(
            body,
            text="Suggested Equation Preview"
        ).pack(fill="x", pady=(0, 6))

        self.preview_editor = CodeEditor(
            body,
            placeholder_text="",
            height=100
        )

        self.preview_editor.pack(
            fill="x",
            pady=(0, Spacing.LG)
        )

        self.preview_editor.set_state("disabled")


        # =========================
        # Suggested Changes
        # =========================

        SectionLabel(
            body,
            text="Suggested Changes"
        ).pack(fill="x", pady=(0, 8))

        self.list_frame = ctk.CTkScrollableFrame(
            body,
            fg_color=Color.TRANSPARENT,
        )

        self.list_frame.pack(
            fill="both",
            expand=True,
            pady=(0, Spacing.MD)
        )

        self.rows = []
        
        actions = ctk.CTkFrame(body, fg_color=Color.TRANSPARENT)
        actions.pack(fill="x")
        OutlineButton(
            actions,
            text="Discard",
            icon=Icon.CLEAR,
            command=self.discard
        ).pack(side="left")

        PrimaryButton(
            actions,
            text="Apply Suggestions",
            icon=Icon.CHECK,
            command=self.apply
        ).pack(side="right")

    def discard(self):

        for row in self.rows:
            row.destroy()

        self.rows.clear()

        self.preview_editor.clear()
        self.preview_editor.set_state("disabled")

        state.results = None
        
    def apply(self):

        if state.results is None:
            return

        state.equation = state.results["new_equation"]

        state.notify()

    def refresh(self):

        if state.results is None:
            return
        
        for row in self.rows:
            row.destroy()

        self.rows.clear()

        priority_color = {
            "High": Color.SUCCESS,
            "Medium": Color.WARNING,
            "Low": Color.TEXT_MUTED
        }

        for rec in state.results["recommendations"]:

            description = (
                f'Incluya la palabra clave "{rec["term"]}" en la ecuación de búsqueda.\n'
                f'{rec["reason"]}'
            )

            row = RecommendationRow(
                self.list_frame,
                Icon.PLUS,
                priority_color[rec["priority"]],
                rec["priority"],
                description
            )

            row.pack(fill="x", pady=5)

            self.rows.append(row)

        self.preview_editor.set_state("normal")

        self.preview_editor.clear()

        self.preview_editor.insert_text(
            state.results["new_equation"]
        )

        self.preview_editor.set_state("disabled")