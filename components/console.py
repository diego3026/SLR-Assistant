"""
console.py
Persistent bottom console panel that mimics an IDE output/terminal pane.
Displays status messages such as "Loading dataset...", "Search completed.".
No process logic is wired here — only the visual log and an append() API
that the future backend can call.
"""

import tkinter as tk
import customtkinter as ctk
from styles.theme import Color, Font, Icon, Radius, Spacing

LEVEL_COLORS = {
    "info": Color.TEXT_SECONDARY,
    "success": Color.SUCCESS,
    "warning": Color.WARNING,
    "error": Color.DANGER,
    "system": Color.PRIMARY,
}


class Console(ctk.CTkFrame):
    """Collapsible-looking terminal panel pinned to the bottom of the window."""

    def __init__(self, master, height=170, **kwargs):
        super().__init__(
            master,
            fg_color=Color.BG_CONSOLE,
            corner_radius=0,
            height=height,
            **kwargs,
        )
        self.pack_propagate(False)

        # Top divider
        ctk.CTkFrame(self, fg_color=Color.BORDER_SOFT, height=1).pack(side="top", fill="x")

        header = ctk.CTkFrame(self, fg_color=Color.TRANSPARENT, height=32)
        header.pack(fill="x", padx=Spacing.LG, pady=(Spacing.SM, 0))

        ctk.CTkLabel(
            header, text=f"{Icon.CONSOLE}  CONSOLE", font=Font.small(),
            text_color=Color.TEXT_MUTED
        ).pack(side="left")

        status_dot = ctk.CTkLabel(
            header, text=f"{Icon.DOT} Ready", font=Font.small(), text_color=Color.SUCCESS
        )
        status_dot.pack(side="right")

        self.log_box = tk.Text(
            self,
            bg=Color.BG_CONSOLE,
            fg=Color.TEXT_SECONDARY,
            bd=0,
            highlightthickness=0,
            font=("Consolas", 12),
            wrap="word",
            padx=Spacing.LG,
            pady=Spacing.SM,
            state="disabled",
        )
        self.log_box.pack(fill="both", expand=True, padx=(Spacing.SM, Spacing.SM), pady=(4, Spacing.SM))

        for level, color in LEVEL_COLORS.items():
            self.log_box.tag_configure(level, foreground=color)

        # Sample demo log to showcase the visual state
        self._seed_demo_log()

    def _seed_demo_log(self):
        demo_entries = [
            ("system", "SearchAI console initialized."),
        ]
        for level, message in demo_entries:
            self.append(message, level)

    def append(self, message, level="info"):
        """Append a timestamped log line. Ready for backend wiring later."""
        prefix = {
            "info": Icon.TERMINAL,
            "success": Icon.CHECK,
            "warning": "!",
            "error": Icon.CLEAR,
            "system": Icon.MODEL,
        }.get(level, Icon.TERMINAL)

        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{prefix}  {message}\n", level)
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def clear(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
