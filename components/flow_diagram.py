"""
flow_diagram.py
Vertical pipeline/flow diagram used to visualize the model's processing
stages (e.g. CSV Dataset -> Preprocessing -> Embeddings -> ... -> Category).
Purely presentational: a fixed list of steps rendered as connected boxes.
"""

import customtkinter as ctk
from numpy.ma import inner
from styles.theme import Color, Font, Icon, Radius, Spacing

class FlowDiagram(ctk.CTkFrame):
    """
    Renders a vertical sequence of stage boxes connected by arrows.

    `steps` is a list of dicts: {"title": str, "subtitle": str|None,
    "accent": color|None, "highlight": bool}. `highlight=True` makes the
    box stand out (used for the most "impressive" stage, e.g. the model).
    """

    def __init__(self, master, steps, **kwargs):
        super().__init__(master, fg_color=Color.TRANSPARENT, **kwargs)
        self._build(steps)

    def _build(self, steps):
        for i, step in enumerate(steps):
            title = step.get("title", "")
            subtitle = step.get("subtitle")
            accent = step.get("accent", Color.BORDER)
            highlight = step.get("highlight", False)

            box = ctk.CTkFrame(
                self,
                fg_color=Color.BG_CARD_HOVER if highlight else Color.BG_INPUT,
                corner_radius=Radius.LG,
                border_width=2 if highlight else 1,
                border_color=accent,
            )

            box.pack(
                fill="x",
                padx=70,
                pady=2
            )
            inner = ctk.CTkFrame(
                box,
                fg_color=Color.TRANSPARENT
            )

            inner.pack(
                fill="x",
                padx=20,
                pady=12
            )

            ctk.CTkLabel(
                inner,
                text=title,
                font=Font.body_bold(),
                text_color=Color.TEXT_PRIMARY,
                anchor="center",
            ).pack(fill="x")

            if subtitle:
                ctk.CTkLabel(
                    inner,
                    text=subtitle,
                    font=Font.small(),
                    text_color=accent if highlight else Color.TEXT_MUTED,
                    justify="center",
                    wraplength=500,
                ).pack(
                    fill="x",
                    pady=(4,0)
                )

            if i < len(steps) - 1:
                ctk.CTkLabel(
                    self,
                    text="⬇",
                    font=("Segoe UI Symbol",18),
                    text_color=Color.PRIMARY
                ).pack(
                    pady=4
                )