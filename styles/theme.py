"""
theme.py
Centralized design tokens for SearchAI.
Keeping every color, font and spacing value in one place makes the UI
consistent and trivial to re-skin later.
"""

import customtkinter as ctk


class Color:
    """Application color palette."""

    # Base surfaces
    BG_MAIN = "#1E1E1E"        # Main window background
    BG_SIDEBAR = "#252526"     # Left navigation panel
    BG_CARD = "#2D2D30"        # Cards / panels
    BG_CARD_HOVER = "#333336"  # Card hover state
    BG_INPUT = "#1B1B1C"       # Text inputs / editors
    BG_CONSOLE = "#181818"     # Bottom console panel

    # Borders / dividers
    BORDER = "#3A3A3D"
    BORDER_SOFT = "#2A2A2C"

    # Buttons
    PRIMARY = "#3B82F6"
    PRIMARY_HOVER = "#2F6FDB"
    SECONDARY = "#404040"
    SECONDARY_HOVER = "#4C4C4C"

    # Text
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B3B3B3"
    TEXT_MUTED = "#7A7A7C"

    # Status / accents
    SUCCESS = "#22C55E"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"
    INFO = "#3B82F6"

    # Transparent helper for CTk widgets
    TRANSPARENT = "transparent"


class Font:
    """Typography scale. Instantiated lazily (needs a Tk root)."""

    _family = "Segoe UI"
    _mono = "Consolas"

    @classmethod
    def h1(cls):
        return ctk.CTkFont(family=cls._family, size=26, weight="bold")

    @classmethod
    def h2(cls):
        return ctk.CTkFont(family=cls._family, size=20, weight="bold")

    @classmethod
    def h3(cls):
        return ctk.CTkFont(family=cls._family, size=16, weight="bold")

    @classmethod
    def subtitle(cls):
        return ctk.CTkFont(family=cls._family, size=13)

    @classmethod
    def body(cls):
        return ctk.CTkFont(family=cls._family, size=13)

    @classmethod
    def body_bold(cls):
        return ctk.CTkFont(family=cls._family, size=13, weight="bold")

    @classmethod
    def small(cls):
        return ctk.CTkFont(family=cls._family, size=11)

    @classmethod
    def button(cls):
        return ctk.CTkFont(family=cls._family, size=13, weight="bold")

    @classmethod
    def nav(cls):
        return ctk.CTkFont(family=cls._family, size=14)

    @classmethod
    def mono(cls):
        return ctk.CTkFont(family=cls._mono, size=13)

    @classmethod
    def mono_small(cls):
        return ctk.CTkFont(family=cls._mono, size=12)

    @classmethod
    def kpi_value(cls):
        return ctk.CTkFont(family=cls._family, size=28, weight="bold")


class Spacing:
    """Consistent spacing scale (px)."""
    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32


class Radius:
    """Corner radius scale."""
    SM = 6
    MD = 10
    LG = 14


class Icon:
    """
    Unicode glyph icons.
    No external icon assets are required, keeping the app self-contained.
    Swap these for CTkImage-based icon files in /assets later if desired.
    """
    LOGO = "\u2726"          # ✦
    DASHBOARD = "\u25A6"     # ▦
    EQUATION = "\u2318"      # ⌘ (used as "code/query" glyph)
    DATASET = "\u25A3"       # ▣
    RECOMMEND = "\u2728"     # ✨
    HISTORY = "\u21BA"       # ↺
    SETTINGS = "\u2699"      # ⚙
    SEARCH = "\u2315"        # ⌕
    SAVE = "\u2913"          # ⤓
    OPEN = "\u2192"          # →
    CLEAR = "\u2715"         # ✕
    PLAY = "\u25B6"          # ▶
    CHECK = "\u2713"         # ✓
    UPLOAD = "\u2B06"        # ⬆
    RESTORE = "\u21BA"       # ↺
    PLUS = "\u002B"          # +
    MINUS = "\u2212"         # −
    ARROW_RIGHT = "\u2192"   # →
    DOT = "\u25CF"           # ●
    TERMINAL = "\u276F"      # ❯
    MODEL = "\u25C6"         # ◆
    CONSOLE = "\u2261"       # ≡
    EVALUATE = "\u2699"      # ⚙
    AI = "🧠"

    MODEL = "🤖"

    CHART = "📈"