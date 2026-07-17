"""
info_tile.py
Small read-only label/value tile, reused across views to display static
metadata (dataset summary, model metrics, etc.).
"""

import customtkinter as ctk
from styles.theme import Color, Font, Radius, Spacing


class InfoTile(ctk.CTkFrame):
    """A compact card showing a label on top and a value below it."""

    def __init__(self, master, label, value, accent=Color.TEXT_PRIMARY, icon="", **kwargs):
        super().__init__(
            master, fg_color=Color.BG_INPUT, corner_radius=Radius.MD,
            border_width=1, border_color=Color.BORDER, **kwargs
        )
        inner = ctk.CTkFrame(self, fg_color=Color.TRANSPARENT)
        inner.pack(fill="both", expand=True, padx=Spacing.MD, pady=Spacing.MD)

        ctk.CTkLabel(
            inner, text=label.upper(), font=Font.small(), text_color=Color.TEXT_MUTED, anchor="w"
        ).pack(fill="x")

        value_row = ctk.CTkFrame(inner, fg_color=Color.TRANSPARENT)
        value_row.pack(fill="x", pady=(4, 0))

        if icon:
            ctk.CTkLabel(
                value_row, text=icon, font=Font.h3(), text_color=accent, width=20
            ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            value_row, text=value, font=Font.h3(), text_color=accent, anchor="w"
        ).pack(side="left", fill="x")