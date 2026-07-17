"""
sidebar.py
Left navigation panel (250px) with the SearchAI logo and primary nav items.
"""

import customtkinter as ctk
from styles.theme import Color, Font, Icon, Spacing, Radius


NAV_ITEMS = [
    ("dashboard", Icon.DASHBOARD, "Dashboard"),
    ("search_equation", Icon.EQUATION, "Search Equation"),
    ("dataset", Icon.DATASET, "Dataset"),
    ("ai_analysis", Icon.AI, "AI Analysis"),
    ("recommendations", Icon.RECOMMEND, "Recommendations"),
    ("history", Icon.HISTORY, "History"),
    ("ai_model_evaluation", Icon.EVALUATE, "AI Model Evaluation"),
]

class Sidebar(ctk.CTkFrame):
    """
    Vertical navigation bar. Calls `on_navigate(key)` whenever the user
    selects a different section. Purely visual — no routing logic here.
    """

    def __init__(self, master, on_navigate=None, **kwargs):
        super().__init__(
            master,
            width=250,
            fg_color=Color.BG_SIDEBAR,
            corner_radius=0,
            **kwargs,
        )
        self.pack_propagate(False)
        self.on_navigate = on_navigate
        self.nav_buttons = {}
        self.active_key = "dashboard"

        self._build_logo()
        self._build_nav()

    def _build_logo(self):
        logo_frame = ctk.CTkFrame(self, fg_color=Color.TRANSPARENT, height=70)
        logo_frame.pack(fill="x", padx=Spacing.LG, pady=(Spacing.LG, Spacing.SM))
        logo_frame.pack_propagate(False)

        row = ctk.CTkFrame(logo_frame, fg_color=Color.TRANSPARENT)
        row.pack(fill="both", expand=True)

        ctk.CTkLabel(
            row, text=Icon.LOGO, font=Font.h2(), text_color=Color.PRIMARY, width=28
        ).pack(side="left")

        text_col = ctk.CTkFrame(row, fg_color=Color.TRANSPARENT)
        text_col.pack(side="left", padx=(Spacing.SM, 0))

        ctk.CTkLabel(
            text_col, text="SearchAI", font=Font.h2(), text_color=Color.TEXT_PRIMARY, anchor="w"
        ).pack(fill="x")
        ctk.CTkLabel(
            text_col, text="Literature Review Assistant", font=Font.small(),
            text_color=Color.TEXT_MUTED, anchor="w"
        ).pack(fill="x")

        # Divider
        ctk.CTkFrame(self, fg_color=Color.BORDER_SOFT, height=1).pack(
            fill="x", padx=Spacing.LG, pady=(Spacing.SM, Spacing.MD)
        )

    def _build_nav(self):
        nav_container = ctk.CTkFrame(self, fg_color=Color.TRANSPARENT)
        nav_container.pack(fill="both", expand=True, padx=Spacing.SM)

        for key, icon, label in NAV_ITEMS:
            self._make_nav_button(nav_container, key, icon, label)

    def _make_nav_button(self, parent, key, icon, label):
        btn = ctk.CTkButton(
            parent,
            text=f"  {icon}    {label}",
            anchor="w",
            font=Font.nav(),
            height=42,
            corner_radius=Radius.SM,
            fg_color=Color.PRIMARY if key == self.active_key else Color.TRANSPARENT,
            hover_color=Color.BG_CARD_HOVER,
            text_color=Color.TEXT_PRIMARY,
            command=lambda k=key: self._handle_click(k),
        )
        btn.pack(fill="x", pady=3)
        self.nav_buttons[key] = btn

    def _handle_click(self, key):
        self.set_active(key)
        if self.on_navigate:
            self.on_navigate(key)

    def set_active(self, key):
        self.active_key = key

        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(
                    fg_color=Color.PRIMARY,
                    text_color=Color.TEXT_PRIMARY
                )
            else:
                btn.configure(
                    fg_color=Color.TRANSPARENT,
                    text_color=Color.TEXT_PRIMARY
                )