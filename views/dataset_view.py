"""
dataset_view.py
Section 3 — Dataset.
Shows dataset summary info (article count, source database, import date)
and dataset management actions.
"""

import customtkinter as ctk
from styles.theme import Color, Font, Icon, Spacing, Radius
from components.card import Card, SectionLabel
from components.buttons import PrimaryButton, SecondaryButton, DangerButton
import os
import pandas as pd

from datetime import datetime
from tkinter import filedialog, messagebox

from services.app_state import state
from services.search_engine import SearchEngine
from services.console_service import console

class InfoTile(ctk.CTkFrame):
    """Small read-only info tile."""

    def __init__(self, master, label, value="", accent=Color.TEXT_PRIMARY, **kwargs):
        super().__init__(
            master,
            fg_color=Color.BG_INPUT,
            corner_radius=Radius.MD,
            border_width=1,
            border_color=Color.BORDER,
            **kwargs,
        )

        inner = ctk.CTkFrame(self, fg_color=Color.TRANSPARENT)
        inner.pack(fill="both", expand=True, padx=Spacing.MD, pady=Spacing.MD)

        ctk.CTkLabel(
            inner,
            text=label.upper(),
            font=Font.small(),
            text_color=Color.TEXT_MUTED,
            anchor="w",
        ).pack(fill="x")

        self.value_label = ctk.CTkLabel(
            inner,
            text=value,
            font=Font.h3(),
            text_color=accent,
            anchor="w",
        )

        self.value_label.pack(fill="x", pady=(4, 0))

    def set_value(self, value):
        self.value_label.configure(text=str(value))


class DatasetView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Color.TRANSPARENT, **kwargs)
        self.engine = SearchEngine()
        self._build()

    def _build(self):
        card = Card(
            self,
            title="Dataset",
            subtitle="Import and validate the Scopus CSV that will be analyzed by the AI model.",
            icon=Icon.DATASET,
        )
        card.pack(fill="both", expand=True, padx=Spacing.XL, pady=Spacing.LG)

        body = card.body

        SectionLabel(body, text="Dataset Summary").pack(fill="x", pady=(0, 10))

        summary_row = ctk.CTkFrame(body, fg_color=Color.TRANSPARENT)
        summary_row.pack(fill="x", pady=(0, Spacing.LG))
        summary_row.grid_columnconfigure((0, 1, 2), weight=1, uniform="tile")

        self.articles_tile = InfoTile(
            summary_row,
            "Number of Articles",
            "-",
            Color.PRIMARY
        )

        self.articles_tile.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )
        
        self.database_tile = InfoTile(
            summary_row,
            "Source Database",
            "-"
        )

        self.database_tile.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=8
        )

        self.date_tile = InfoTile(
            summary_row,
            "Import Date",
            "-"
        )

        self.date_tile.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(8, 0)
        )

        # Actions
        actions = ctk.CTkFrame(body, fg_color=Color.TRANSPARENT)
        actions.pack(fill="x")

        PrimaryButton(
            actions,
            text="Import CSV",
            icon=Icon.UPLOAD,
            command=self.import_csv
        ).pack(side="left")

        SecondaryButton(
            actions,
            text="Open Dataset",
            icon=Icon.OPEN,
            command=self.open_dataset
        ).pack(side="left", padx=(Spacing.SM,0))

        PrimaryButton(
            actions,
            text="Analyze Dataset",
            icon=Icon.PLAY,
            command=self.analyze_dataset
        ).pack(side="right")

        DangerButton(
            actions,
            text="Clear",
            icon=Icon.CLEAR,
            command=self.clear_dataset
        ).pack(side="right", padx=(0, Spacing.SM))

    def clear_dataset(self):

        state.csv_path = ""
        state.results = None

        self.articles_tile.set_value("-")
        self.database_tile.set_value("-")
        self.date_tile.set_value("-")

        messagebox.showinfo(
            "Dataset",
            "Dataset removed."
        )

    def analyze_dataset(self):
        console.info("Analyzing dataset...")

        if state.csv_path == "":
            messagebox.showerror(
                "Dataset",
                "Load a CSV first."
            )
            return

        if state.topic == "":
            messagebox.showerror(
                "Context",
                "Save the research context first."
            )
            return

        if state.equation == "":
            messagebox.showerror(
                "Equation",
                "Save the search equation first."
            )
            return

        self.configure(cursor="watch")
        
        self.update_idletasks()

        results = self.engine.run(
            csv_path=state.csv_path,
            topic=state.topic,
            objectives=state.objectives,
            notes=state.notes,
            equation=state.equation
        )

        self.configure(cursor="")
        
        state.results = results

        stats = results["statistics"]

        state.history.append(
            {
                "iteration": f"#{len(state.history)+1}",
                "equation": state.equation,
                "total":stats["total_articles"],
                "high":stats["highly_relevant"],
                "relevant":stats["relevant"],
                "date": datetime.now().strftime("%Y-%m-%d")
            }

        )
        state.notify()

        console.success("Analysis completed successfully.")
        messagebox.showinfo(
            "SearchAI",
            "Analysis completed successfully."
        )

    def open_dataset(self):
        if state.csv_path == "":
            messagebox.showwarning(
                "Dataset",
                "No dataset loaded."
            )
            return

        os.startfile(state.csv_path)

    def import_csv(self):
        console.info("Importing dataset...")

        filename = filedialog.askopenfilename(
            title="Select Scopus CSV",
            filetypes=[("CSV","*.csv")]
        )

        if not filename:
            return

        state.csv_path = filename
        df = pd.read_csv(filename)

        required_columns = [
            "Title",
            "Abstract",
            "Author Keywords"
        ]

        missing = [
            c for c in required_columns
            if c not in df.columns
        ]

        if missing:
            messagebox.showerror(
                "Invalid CSV",
                "Missing columns:\n\n" + "\n".join(missing)
            )
            return

        self.articles_tile.set_value(len(df))
        database = os.path.basename(filename)

        if "scopus" in database.lower():
            database = "Scopus"

        elif "ieee" in database.lower():
            database = "IEEE Xplore"

        self.database_tile.set_value(database)
        self.date_tile.set_value(
            datetime.now().strftime("%Y-%m-%d")
        )

        console.success("Dataset imported successfully.")
        messagebox.showinfo("Dataset", "Dataset imported successfully.")