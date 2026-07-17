"""
kpi_card.py
Small metric cards used in the AI Analysis dashboard
(e.g. Relevant Papers, Confidence, Coverage).
"""

import customtkinter as ctk
from styles.theme import Color, Font, Radius, Spacing


class KPICard(ctk.CTkFrame):

    def __init__(
        self,
        master,
        label="Metric",
        value="0",
        accent=Color.PRIMARY,
        suffix="",
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=Color.BG_CARD,
            corner_radius=Radius.MD,
            border_width=1,
            border_color=Color.BORDER_SOFT,
            height=90,
            **kwargs
        )

        # IMPORTANTE
        self.grid_propagate(False)
        self.pack_propagate(False)

        strip = ctk.CTkFrame(
            self,
            fg_color=accent,
            width=4,
            corner_radius=2
        )
        strip.pack(
            side="left",
            fill="y",
            pady=12
        )

        content = ctk.CTkFrame(
            self,
            fg_color=Color.TRANSPARENT
        )
        content.pack(
            side="left",
            fill="both",
            expand=True,
            padx=14,
            pady=12
        )

        ctk.CTkLabel(
            content,
            text=label.upper(),
            font=Font.small(),
            text_color=Color.TEXT_MUTED,
            anchor="w"
        ).pack(anchor="w")

        self.value_label = ctk.CTkLabel(
            content,
            text=str(value),
            font=Font.h2(),
            text_color=Color.TEXT_PRIMARY,
            anchor="w"
        )
        self.value_label.pack(anchor="w", pady=(6,0))

        if suffix:
            ctk.CTkLabel(
                content,
                text=suffix,
                font=Font.body(),
                text_color=accent
            ).pack(anchor="w")

    def set_value(self, value):
        self.value_label.configure(text=str(value))