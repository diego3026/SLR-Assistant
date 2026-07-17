"""
dashboard_view.py
Section 1 — Research Context.
Landing page where the user defines the topic, objectives and notes
that will guide the AI throughout the review.
"""

import customtkinter as ctk
from styles.theme import Color, Font, Icon, Spacing
from components.card import Card, SectionLabel
from components.buttons import PrimaryButton
from services.app_state import state
from tkinter import messagebox
from services.console_service import console

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Color.TRANSPARENT, **kwargs)
        self._build()

    def _build(self):
        card = Card(
            self,
            title="Research Context",
            subtitle="Define the scope of your systematic literature review.",
            icon=Icon.DASHBOARD,
        )
        card.pack(fill="both", expand=True, padx=Spacing.XL, pady=Spacing.LG)

        body = card.body

        # Research Topic
        SectionLabel(body, text="Research Topic").pack(fill="x", pady=(0, 6))
        self.topic_box = ctk.CTkTextbox(
            body, height=40, fg_color=Color.BG_INPUT, border_width=1,
            border_color=Color.BORDER, corner_radius=8, font=Font.body(),
            text_color=Color.TEXT_PRIMARY,
        )
        self.topic_box.pack(fill="x", pady=(0, Spacing.MD))
        self.topic_box.insert(
            "1.0",
            "Application of machine learning techniques for early diagnosis "
            "of cardiovascular diseases."
        )

        # Objectives
        SectionLabel(body, text="Objectives").pack(fill="x", pady=(0, 6))
        self.objectives_box = ctk.CTkTextbox(
            body, height=70, fg_color=Color.BG_INPUT, border_width=1,
            border_color=Color.BORDER, corner_radius=8, font=Font.body(),
            text_color=Color.TEXT_PRIMARY,
        )
        self.objectives_box.pack(fill="x", pady=(0, Spacing.MD))
        self.objectives_box.insert(
            "1.0",
            "1. Identify ML models used for cardiovascular risk prediction.\n"
            "2. Compare reported accuracy across studies.\n"
            "3. Detect research gaps for future work."
        )

        # Notes
        SectionLabel(body, text="Notes").pack(fill="x", pady=(0, 6))
        self.notes_box = ctk.CTkTextbox(
            body, height=60, fg_color=Color.BG_INPUT, border_width=1,
            border_color=Color.BORDER, corner_radius=8, font=Font.body(),
            text_color=Color.TEXT_PRIMARY,
        )
        self.notes_box.pack(fill="x", pady=(0, Spacing.LG))
        self.notes_box.insert(
            "1.0",
            "Focus on studies published after 2018. Exclude reviews without "
            "primary data."
        )

        # Actions
        actions = ctk.CTkFrame(body, fg_color=Color.TRANSPARENT)
        actions.pack(fill="x")
        PrimaryButton(actions, text="Save Context", icon=Icon.SAVE, command=self.save_context).pack(side="right")

    def save_context(self):

        state.topic = self.topic_box.get("1.0", "end").strip()
        state.objectives = self.objectives_box.get("1.0", "end").strip()
        state.notes = self.notes_box.get("1.0", "end").strip()

        console.success("Research context saved.")
        messagebox.showinfo(
            "SearchAI",
            "Research context saved."
        )