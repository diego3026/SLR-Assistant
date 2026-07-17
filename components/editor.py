"""
editor.py
A VSCode-style code editor widget with line numbers and basic static
syntax highlighting for boolean search operators. Purely presentational —
highlighting is re-applied on keystroke, no query logic is implemented.
"""

import tkinter as tk
import customtkinter as ctk
from sympy import content
from styles.theme import Color, Font, Radius, Spacing

KEYWORDS = ("AND", "OR", "NOT")


class CodeEditor(ctk.CTkFrame):
    """Multi-line text editor styled like an IDE, with a line-number gutter."""

    def __init__(self, master, placeholder_text="", height=220, **kwargs):
        super().__init__(
            master,
            height=height,
            fg_color=Color.BG_INPUT,
            corner_radius=Radius.MD,
            border_width=1,
            border_color=Color.BORDER,
            **kwargs,
        )
        self.pack_propagate(False)

        wrapper = ctk.CTkFrame(self, fg_color=Color.TRANSPARENT)
        wrapper.pack(fill="both", padx=1, pady=1)

        # Line-number gutter
        self.gutter = tk.Text(
            wrapper,
            width=4,
            padx=8,
            pady=10,
            bg=Color.BG_INPUT,
            fg=Color.TEXT_MUTED,
            bd=0,
            highlightthickness=0,
            font=("Consolas", 13),
            state="disabled",
            takefocus=False,
        )
        self.gutter.pack(side="left", fill="y")

        # Main text area
        self.text = tk.Text(
            wrapper,
            bg=Color.BG_INPUT,
            fg=Color.TEXT_PRIMARY,
            insertbackground=Color.PRIMARY,
            selectbackground=Color.PRIMARY,
            selectforeground=Color.TEXT_PRIMARY,
            bd=0,
            highlightthickness=0,
            font=("Consolas", 13),
            wrap="none",
            padx=6,
            pady=10,
            height=height // 20,
            undo=True,
        )
        self.text.pack(side="left", fill="both")

        # Tag styles for basic highlighting
        self.text.tag_configure("keyword", foreground=Color.PRIMARY)
        self.text.tag_configure("string", foreground=Color.SUCCESS)
        self.text.tag_configure("comment", foreground=Color.TEXT_MUTED)

        if placeholder_text:
            self.text.insert("1.0", placeholder_text)

        self.text.bind("<KeyRelease>", self._on_change)
        self._refresh_gutter()
        self._highlight()

    # ------------------------------------------------------------------
    def _on_change(self, event=None):
        self._refresh_gutter()
        self._highlight()

    def _refresh_gutter(self):
        line_count = int(self.text.index("end-1c").split(".")[0])
        numbers = "\n".join(str(i) for i in range(1, line_count + 1))
        self.gutter.configure(state="normal")
        self.gutter.delete("1.0", "end")
        self.gutter.insert("1.0", numbers)
        self.gutter.configure(state="disabled")

    def _highlight(self):
        for tag in ("keyword", "string"):
            self.text.tag_remove(tag, "1.0", "end")

        content = self.text.get("1.0", "end-1c")
        for keyword in KEYWORDS:
            start = "1.0"
            while True:
                pos = self.text.search(rf"\y{keyword}\y", start, stopindex="end", regexp=True)
                if not pos:
                    break
                end = f"{pos}+{len(keyword)}c"
                self.text.tag_add("keyword", pos, end)
                start = end

        # Highlight quoted strings
        start = "1.0"
        while True:
            pos = self.text.search('"', start, stopindex="end")
            if not pos:
                break
            end_pos = self.text.search('"', f"{pos}+1c", stopindex="end")
            if not end_pos:
                break
            end_pos = f"{end_pos}+1c"
            self.text.tag_add("string", pos, end_pos)
            start = end_pos

    # ------------------------------------------------------------------
    def get_text(self):
        return self.text.get("1.0", "end-1c")

    def set_text(self, content):
        self.insert_text(content)

    # ------------------------------------------------------------------
    def set_state(self, state):
        """
        Cambia el estado del editor.
        state = "normal" | "disabled"
        """
        self.text.configure(state=state)

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self._on_change()

    def insert_text(self, content):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)
        self._on_change()

    def delete(self, start="1.0", end="end"):
        self.text.delete(start, end)
        self._on_change()

    def insert(self, index, text):
        self.text.insert(index, text)
        self._on_change()

    def get(self, start="1.0", end="end-1c"):
        return self.text.get(start, end)