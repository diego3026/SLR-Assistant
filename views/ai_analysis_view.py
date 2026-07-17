"""
ai_analysis_view.py
Section 4 — AI Analysis.
KPI cards, progress indicator and a results table with per-article
relevance scoring produced by the (future) AI model.
"""

import customtkinter as ctk
from styles.theme import Color, Font, Icon, Spacing
from components.card import Card, SectionLabel
from components.kpi_card import KPICard
from components.table import DataTable
from services.app_state import state

COLUMNS = [
    ("rank", "#", 50),
    ("title", "Title", 430),
    ("similarity", "Similarity", 90),
    ("category", "Category", 150),
    ("keywords", "Author Keywords", 260),
]

class AIAnalysisView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Color.TRANSPARENT, **kwargs)
        self._build()
        state.subscribe(self.refresh)

    def _build(self):
        card = Card(
            self,
            title="AI Analysis",
            subtitle="Semantic relevance analysis using BAAI/bge-small-en-v1.5 embeddings.",
            icon=Icon.AI,
        )
        card.pack(fill="both", expand=True, padx=Spacing.XL, pady=Spacing.LG)

        body = card.body

        # KPI row
        kpi_row = ctk.CTkFrame(body, fg_color=Color.TRANSPARENT, height=80)
        kpi_row.pack(fill="x", pady=(0, 8))
        kpi_row.grid_columnconfigure((0,1,2,3), weight=1, uniform="kpi")
        kpi_row.grid_rowconfigure(0, weight=0)

        self.total_card = KPICard(
            kpi_row,
            "Total Articles",
            "0",
            Color.PRIMARY
        )

        self.total_card.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0,8)
        )

        self.high_card = KPICard(
            kpi_row,
            "Highly Relevant",
            "0",
            Color.SUCCESS
        )

        self.high_card.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=8
        )

        self.rel_card = KPICard(
            kpi_row,
            "Relevant",
            "0",
            Color.WARNING
        )

        self.rel_card.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=8
        )

        self.noise_card = KPICard(
            kpi_row,
            "Noise",
            "0",
            Color.DANGER
        )

        self.noise_card.grid(
            row=0,
            column=3,
            sticky="ew",
            padx=(8,0)
        )

        # Progress bar
        SectionLabel(body, text="Analysis Progress").pack(fill="x", pady=(8, 4))
        progress_row = ctk.CTkFrame(body, fg_color=Color.TRANSPARENT)
        progress_row.pack(fill="x", pady=(0, 8))

        self.progress = ctk.CTkProgressBar(
            progress_row, progress_color=Color.PRIMARY, fg_color=Color.BG_INPUT, height=10
        )
        self.progress.pack(side="left", fill="x", expand=True)
        self.progress.set(0)

        self.progress_label = ctk.CTkLabel(
            progress_row,
            text="0%",
            font=Font.small(),
            text_color=Color.TEXT_SECONDARY
        )

        self.progress_label.pack(
            side="left",
            padx=(Spacing.SM,0)
        )

        # Results table
        SectionLabel(body, text="Scored Articles").pack(fill="x", pady=(8, 4))
        self.table = DataTable(
            body,
            COLUMNS,
            [],
            height=18
        )

        self.table.pack(
            fill="both",
            expand=True
        )

    def refresh(self):
        if state.results is None:
            return

        dataframe = state.results["dataframe"].sort_values(
            "Similarity",
            ascending=False
        )

        self.load_statistics(state.results["statistics"])
        self.load_table(dataframe)

    def load_statistics(self, stats):

        self.total_card.set_value(
            stats["total_articles"]
        )

        self.high_card.set_value(
            stats["highly_relevant"]
        )

        self.rel_card.set_value(
            stats["relevant"]
        )

        self.noise_card.set_value(
            stats["noise"]
        )

        progress = 0

        if stats["total_articles"] > 0:
            progress = (
                stats["highly_relevant"] +
                stats["relevant"]
            ) / stats["total_articles"]

        self.progress.set(progress)

        self.progress_label.configure(
            text=f"{progress*100:.0f}%"
        )

    def load_table(self, dataframe):

        rows = []

        for rank, (_, row) in enumerate(dataframe.iterrows(), start=1):

            keywords = row.get("Author Keywords", "")

            if keywords != keywords:
                keywords = ""

            keywords = str(keywords)

            if len(keywords) > 80:
                keywords = keywords[:77] + "..."

            rows.append(
                {
                    "rank": rank,
                    "title": row["Title"],
                    "similarity": f'{row["Similarity"]:.3f}',
                    "category": row["Category"],
                    "keywords": keywords
                }
            )

        self.table.load_rows(
            COLUMNS,
            rows
        )