"""
header.py
Application header.
Shows:
- Current section
- Subtitle
- AI model (fixed)
- Loaded dataset
"""

import os
import customtkinter as ctk

from styles.theme import Color, Font, Icon, Spacing, Radius
from services.app_state import state


class Header(ctk.CTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(
            master,
            fg_color=Color.TRANSPARENT,
            height=100,
            **kwargs
        )

        self.pack_propagate(False)

        state.subscribe(self.refresh)

        divider = ctk.CTkFrame(
            self,
            fg_color=Color.BORDER_SOFT,
            height=1
        )

        divider.pack(
            side="bottom",
            fill="x"
        )

        content = ctk.CTkFrame(
            self,
            fg_color=Color.TRANSPARENT
        )

        content.pack(
            fill="both",
            expand=True,
            padx=Spacing.XL,
            pady=Spacing.MD
        )

        # -------------------------
        # LEFT
        # -------------------------

        left = ctk.CTkFrame(
            content,
            fg_color=Color.TRANSPARENT
        )

        left.pack(
            side="left",
            fill="y"
        )

        self.title_label = ctk.CTkLabel(
            left,
            text="SearchAI",
            font=Font.h1(),
            text_color=Color.TEXT_PRIMARY
        )

        self.title_label.pack(anchor="w")

        self.subtitle_label = ctk.CTkLabel(
            left,
            text="AI-powered literature review assistant",
            font=Font.subtitle(),
            text_color=Color.TEXT_MUTED
        )

        self.subtitle_label.pack(anchor="w")

        # -------------------------
        # RIGHT
        # -------------------------

        right = ctk.CTkFrame(
            content,
            fg_color=Color.TRANSPARENT
        )

        right.pack(
            side="right"
        )

        info = ctk.CTkFrame(
            right,
            fg_color=Color.BG_CARD,
            corner_radius=Radius.MD,
            border_width=1,
            border_color=Color.BORDER
        )

        info.pack()

        inner = ctk.CTkFrame(
            info,
            fg_color=Color.TRANSPARENT
        )

        inner.pack(
            padx=15,
            pady=8
        )

        self.model_label = ctk.CTkLabel(
            inner,
            text="🤖 BAAI/bge-small-en-v1.5",
            font=Font.body_bold(),
            text_color=Color.SUCCESS
        )

        self.model_label.pack(anchor="e")

        self.dataset_label = ctk.CTkLabel(
            inner,
            text="📄 No dataset loaded",
            font=Font.small(),
            text_color=Color.TEXT_MUTED
        )

        self.dataset_label.pack(anchor="e")

    def set_title(self, title, subtitle):

        self.title_label.configure(text=title)
        self.subtitle_label.configure(text=subtitle)

    def refresh(self):

        if getattr(state, "csv_path", None):

            self.dataset_label.configure(
                text=f"📄 {os.path.basename(state.csv_path)}"
            )

        else:

            self.dataset_label.configure(
                text="📄 No dataset loaded"
            )