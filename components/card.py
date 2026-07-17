"""
card.py
Reusable "card" container used throughout the app to group related content,
mirroring the panel style seen in Notion / GitHub Desktop / Cursor.
"""

import customtkinter as ctk
from styles.theme import Color, Font, Radius, Spacing


class Card(ctk.CTkFrame):
    """
    A rounded panel with an optional title/subtitle header and a body
    frame that child widgets can be packed/gridded into.
    """

    def __init__(self, master, title=None, subtitle=None, icon="", **kwargs):
        super().__init__(
            master,
            fg_color=Color.BG_CARD,
            corner_radius=Radius.LG,
            border_width=1,
            border_color=Color.BORDER_SOFT,
            **kwargs,
        )

        self._header_built = False

        if title:
            self._build_header(title, subtitle, icon)

        # Body: where the caller places its own widgets
        self.body = ctk.CTkFrame(self, fg_color=Color.TRANSPARENT)
        self.body.pack(
            fill="both",
            expand=True,
            padx=Spacing.LG,
            pady=(0 if self._header_built else Spacing.LG, Spacing.LG),
        )

    def _build_header(self, title, subtitle, icon):
        header = ctk.CTkFrame(self, fg_color=Color.TRANSPARENT)
        header.pack(fill="x", padx=Spacing.LG, pady=(Spacing.LG, Spacing.SM))

        title_row = ctk.CTkFrame(header, fg_color=Color.TRANSPARENT)
        title_row.pack(fill="x")

        if icon:
            ctk.CTkLabel(
                title_row, text=icon, font=Font.h3(), text_color=Color.PRIMARY, width=24
            ).pack(side="left", padx=(0, Spacing.SM))

        ctk.CTkLabel(
            title_row, text=title, font=Font.h3(), text_color=Color.TEXT_PRIMARY
        ).pack(side="left")

        if subtitle:
            ctk.CTkLabel(
                header,
                text=subtitle,
                font=Font.small(),
                text_color=Color.TEXT_MUTED,
                anchor="w",
                justify="left",
            ).pack(fill="x", pady=(2, 0))

        self._header_built = True


class SectionLabel(ctk.CTkLabel):
    """Small uppercase label used to introduce a field inside a card."""

    def __init__(self, master, text="", **kwargs):
        super().__init__(
            master,
            text=text.upper(),
            font=Font.small(),
            text_color=Color.TEXT_MUTED,
            anchor="w",
            **kwargs,
        )
