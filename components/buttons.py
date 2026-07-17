"""
buttons.py
Reusable button components with consistent styling across the app.
"""

import customtkinter as ctk
from styles.theme import Color, Font, Radius


class PrimaryButton(ctk.CTkButton):
    """Solid blue call-to-action button (e.g. Save, Run Search)."""

    def __init__(self, master, text="Button", icon="", command=None, width=140, **kwargs):
        label = f"{icon}  {text}" if icon else text
        super().__init__(
            master,
            text=label,
            command=command,
            width=width,
            height=38,
            corner_radius=Radius.SM,
            fg_color=Color.PRIMARY,
            hover_color=Color.PRIMARY_HOVER,
            text_color=Color.TEXT_PRIMARY,
            font=Font.button(),
            **kwargs,
        )


class SecondaryButton(ctk.CTkButton):
    """Neutral gray button for secondary actions (e.g. Load, Cancel)."""

    def __init__(self, master, text="Button", icon="", command=None, width=140, **kwargs):
        label = f"{icon}  {text}" if icon else text
        super().__init__(
            master,
            text=label,
            command=command,
            width=width,
            height=38,
            corner_radius=Radius.SM,
            fg_color=Color.SECONDARY,
            hover_color=Color.SECONDARY_HOVER,
            text_color=Color.TEXT_PRIMARY,
            font=Font.button(),
            **kwargs,
        )


class OutlineButton(ctk.CTkButton):
    """Low-emphasis bordered button for tertiary actions."""

    def __init__(self, master, text="Button", icon="", command=None, width=140, **kwargs):
        label = f"{icon}  {text}" if icon else text
        super().__init__(
            master,
            text=label,
            command=command,
            width=width,
            height=38,
            corner_radius=Radius.SM,
            fg_color=Color.TRANSPARENT,
            hover_color=Color.BG_CARD_HOVER,
            border_width=1,
            border_color=Color.BORDER,
            text_color=Color.TEXT_SECONDARY,
            font=Font.button(),
            **kwargs,
        )


class DangerButton(ctk.CTkButton):
    """Red button for destructive actions (e.g. Clear Dataset)."""

    def __init__(self, master, text="Button", icon="", command=None, width=140, **kwargs):
        label = f"{icon}  {text}" if icon else text
        super().__init__(
            master,
            text=label,
            command=command,
            width=width,
            height=38,
            corner_radius=Radius.SM,
            fg_color=Color.TRANSPARENT,
            hover_color="#3A1F1F",
            border_width=1,
            border_color=Color.DANGER,
            text_color=Color.DANGER,
            font=Font.button(),
            **kwargs,
        )


class IconButton(ctk.CTkButton):
    """Compact square button used for icon-only actions (e.g. settings gear)."""

    def __init__(self, master, icon="", command=None, size=38, **kwargs):
        super().__init__(
            master,
            text=icon,
            command=command,
            width=size,
            height=size,
            corner_radius=Radius.SM,
            fg_color=Color.BG_CARD,
            hover_color=Color.BG_CARD_HOVER,
            text_color=Color.TEXT_PRIMARY,
            font=Font.h3(),
            **kwargs,
        )
