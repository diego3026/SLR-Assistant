import customtkinter as ctk
from styles.theme import Color

class ScrollPage(ctk.CTkScrollableFrame):

    def __init__(self, master, **kwargs):

        kwargs.setdefault("fg_color", Color.BG_MAIN)
        kwargs.setdefault("corner_radius", 0)

        super().__init__(
            master,
            **kwargs
        )

        self.grid_columnconfigure(0, weight=1)