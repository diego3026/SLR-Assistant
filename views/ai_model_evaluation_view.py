"""
ai_model_evaluation_view.py
AI Model Evaluation — dedicated sidebar section (separated by a divider).

Explains and visualizes the actual relevance-scoring pipeline used by
SearchAI: CSV -> preprocessing -> sentence embeddings (BAAI/bge-small-en-v1.5)
-> cosine similarity -> relevance score -> category assignment.

All numbers are static/demo data, ready to be replaced by real pipeline
output later. No confusion matrix is included on purpose: categories are
derived from a similarity threshold, not from labeled ground truth, so a
confusion matrix would be artificial (explained in the note at the bottom).
"""

from matplotlib import pyplot as plt
import numpy as np
import customtkinter as ctk

from styles.theme import Color, Font, Icon, Spacing, Radius
from components.card import Card, SectionLabel
from components.flow_diagram import FlowDiagram
from components.info_tile import InfoTile
from components.table import DataTable
from components.chart import (
    ChartCanvas,
    build_similarity_histogram_figure,
    build_category_bar_figure,
    build_category_pie_figure,
    build_pca_scatter_figure,
    build_similarity_heatmap_figure,
    build_keywords_bar_figure,
    build_threshold_bar_figure,
    THRESHOLDS,
)
from services.app_state import state

PIPELINE_STEPS = [
    {
        "title": "Dataset",
        "subtitle": "Artículos científicos de Scopus / IEEE / ACM",
        "accent": Color.TEXT_MUTED,
    },
    {
        "title": "Text Preprocessing",
        "subtitle": "Limpieza • Tokenización • Normalización",
        "accent": Color.TEXT_MUTED,
    },
    {
        "title": "Sentence Transformer",
        "subtitle": "BAAI/bge-small-en-v1.5",
        "accent": Color.SUCCESS,
        "highlight": True,
    },
    {
        "title": "Embedding Generation",
        "subtitle": "Vectores semánticos de 384 dimensiones",
        "accent": Color.PRIMARY,
    },
    {
        "title": "Cosine Similarity",
        "subtitle": "Artículo vs Contexto de Búsqueda",
        "accent": Color.WARNING,
    },
    {
        "title": "Ranking",
        "subtitle": "Artículos más relevantes primero",
        "accent": Color.SUCCESS,
    },
    {
        "title": "Recommendations",
        "subtitle": "Sugerencias para mejorar la consulta de búsqueda",
        "accent": Color.PRIMARY,
    },
]

TOP_ARTICLES_COLUMNS = [
    ("rank", "#", 50),
    ("title", "Title", 480),
    ("similarity", "Similarity", 110),
    ("category", "Category", 160),
]

def _build_top_articles_rows(metrics=None):

    if metrics is None:
        return []

    dataframe = metrics["dataframe"]

    dataframe = dataframe.sort_values(
        "Similarity",
        ascending=False
    ).head(20)

    rows = []

    for i, (_, row) in enumerate(dataframe.iterrows(), start=1):

        rows.append({
            "rank": str(i),
            "title": row["Title"],
            "similarity": f'{row["Similarity"]:.3f}',
            "category": row["Category"]
        })

    return rows


class AIModelEvaluationView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Color.TRANSPARENT, **kwargs)
        self._build()
        state.subscribe(self.refresh)

    # ------------------------------------------------------------------
    def _build(self):
        scroll = ctk.CTkScrollableFrame(
            self, fg_color=Color.TRANSPARENT,
            scrollbar_button_color=Color.BORDER,
            scrollbar_button_hover_color=Color.SECONDARY_HOVER,
        )
        scroll.pack(fill="both", expand=True, padx=Spacing.XL, pady=Spacing.LG)
        self.scroll_frame = scroll

        self._build_overview_section(scroll)
        self._build_pipeline_section(scroll)
        self._build_evaluation_section(scroll)
        self._build_histogram_section(scroll)
        self._build_category_section(scroll)
        self._build_top_articles_section(scroll)
        self._build_pca_section(scroll)
        self._build_heatmap_section(scroll)
        self._build_keywords_section(scroll)
        self._build_threshold_section(scroll)
        self._build_confusion_matrix_note(scroll)

    def _build_evaluation_section(self, parent):

        card = Card(
            parent,
            title="3. Semantic Retrieval Evaluation",
            subtitle="Performance of the semantic retrieval pipeline.",
            icon=Icon.CHART,
        )

        card.pack(
            fill="x",
            pady=(0, Spacing.LG)
        )

        self.evaluation_grid = ctk.CTkFrame(
            card.body,
            fg_color=Color.TRANSPARENT
        )

        self.evaluation_grid.pack(fill="x")

        for i in range(4):
            self.evaluation_grid.grid_columnconfigure(i, weight=1)

        self._reload_evaluation_tiles()
        
    def _build_overview_section(self, parent):

        card = Card(
            parent,
            title="Modelo de Recuperación Semántica",
            subtitle="Estadísticas del último análisis realizado.",
            icon=Icon.AI,
        )

        card.pack(fill="x", pady=(0, Spacing.LG))

        self.metrics_grid = ctk.CTkFrame(
            card.body,
            fg_color=Color.TRANSPARENT
        )

        self.metrics_grid.pack(fill="x")

        for i in range(4):
            self.metrics_grid.grid_columnconfigure(i, weight=1)

        self.metric_tiles = []

        self._reload_metric_tiles()

    def _reload_evaluation_tiles(self):

        for w in self.evaluation_grid.winfo_children():
            w.destroy()

        metrics = state.model_metrics

        if metrics is None:
            return

        values = [

            (
                "Average Similarity",
                f'{metrics["average_similarity"]:.3f}',
                Color.SUCCESS
            ),

            (
                "Highest Similarity",
                f'{metrics["highest_similarity"]:.3f}',
                Color.PRIMARY
            ),

            (
                "Lowest Similarity",
                f'{metrics["lowest_similarity"]:.3f}',
                Color.DANGER
            ),

            (
                "Threshold",
                f'{metrics["similarity_threshold"]:.2f}',
                Color.WARNING
            ),

            (
                "Relevant",
                str(metrics["relevant_articles"]),
                Color.SUCCESS
            ),

            (
                "Discarded",
                str(metrics["discarded_articles"]),
                Color.DANGER
            ),

            (
                "Embedding Size",
                str(metrics["embedding_size"]),
                Color.PRIMARY
            ),

            (
                "Similarity Metric",
                metrics["similarity_metric"],
                Color.WARNING
            ),
        ]

        for i, (label, value, accent) in enumerate(values):

            row = i // 4
            col = i % 4

            InfoTile(
                self.evaluation_grid,
                label,
                value,
                accent=accent
            ).grid(
                row=row,
                column=col,
                padx=6,
                pady=6,
                sticky="nsew"
            )

    def _reload_metric_tiles(self):

        for widget in self.metrics_grid.winfo_children():
            widget.destroy()

        metrics = state.model_metrics

        if metrics is None:

            values = [
                ("Embedding Model","--",Color.SUCCESS),
                ("Embedding Size","--",Color.PRIMARY),
                ("Similarity Metric","--",Color.WARNING),
                ("Dataset Size","--",Color.TEXT_PRIMARY),
                ("Relevant Articles","--",Color.SUCCESS),
                ("Discarded Articles","--",Color.DANGER),
                ("Similarity Threshold","--",Color.PRIMARY),
                ("Average Similarity","--",Color.WARNING),
                ("Highest Similarity","--",Color.SUCCESS),
                ("Lowest Similarity","--",Color.DANGER),
            ]

        else:

            values = [

                (
                    "Embedding Model",
                    metrics["embedding_model"],
                    Color.SUCCESS
                ),

                (
                    "Embedding Size",
                    f'{metrics["embedding_size"]} dimensions',
                    Color.PRIMARY
                ),

                (
                    "Similarity Metric",
                    metrics["similarity_metric"],
                    Color.WARNING
                ),

                (
                    "Dataset Size",
                    str(metrics["dataset_size"]),
                    Color.TEXT_PRIMARY
                ),

                (
                    "Relevant Articles",
                    str(metrics["relevant_articles"]),
                    Color.SUCCESS
                ),

                (
                    "Discarded Articles",
                    str(metrics["discarded_articles"]),
                    Color.DANGER
                ),

                (
                    "Similarity Threshold",
                    f'{metrics["similarity_threshold"]:.2f}',
                    Color.PRIMARY
                ),

                (
                    "Average Similarity",
                    f'{metrics["average_similarity"]:.3f}',
                    Color.WARNING
                ),

                (
                    "Highest Similarity",
                    f'{metrics["highest_similarity"]:.3f}',
                    Color.SUCCESS
                ),

                (
                    "Lowest Similarity",
                    f'{metrics["lowest_similarity"]:.3f}',
                    Color.DANGER
                ),
            ]

        for i, (label, value, accent) in enumerate(values):

            row = i // 4
            col = i % 4

            InfoTile(
                self.metrics_grid,
                label,
                value,
                accent=accent
            ).grid(
                row=row,
                column=col,
                padx=6,
                pady=6,
                sticky="nsew"
            )
        
    # ------------------------------------------------------------------
    def _build_pipeline_section(self, parent):
        card = Card(
            parent,
            title="1. Model Pipeline",
            subtitle="How each article turns into a relevance score and a category.",
            icon=Icon.MODEL,
        )
        card.pack(fill="x", pady=(0, Spacing.LG))
        FlowDiagram(card.body, PIPELINE_STEPS).pack(pady=(Spacing.SM, 0))

   
    def _build_histogram_section(self, parent):

        card = Card(
            parent,
            title="2. Similarity Distribution",
            subtitle="Distribution of cosine similarity scores.",
            icon=Icon.CHART,
        )

        card.pack(
            fill="x",
            pady=(0,Spacing.LG)
        )

        self.histogram_parent = card.body

        self.histogram_chart = ChartCanvas(
            self.histogram_parent,
            build_similarity_histogram_figure(state.model_metrics)
        )

        self.histogram_chart.pack(
            fill="both",
            expand=True
        )

    def _reload_histogram(self):
        self.histogram_chart.destroy()

        self.histogram_chart = ChartCanvas(
            self.histogram_parent,
            build_similarity_histogram_figure(
                state.model_metrics
            )
        )

        self.histogram_chart.pack(
            fill="both",
            expand=True
        )

    def _build_category_section(self, parent):

        card = Card(
            parent,
            title="3–4. Category Distribution",
            subtitle="Distribution of the articles classified by the semantic retrieval engine.",
            icon=Icon.CHART,
        )

        card.pack(
            fill="x",
            pady=(0,Spacing.LG)
        )

        row = ctk.CTkFrame(
            card.body,
            fg_color=Color.TRANSPARENT
        )

        row.pack(
            fill="both",
            expand=True
        )

        row.grid_columnconfigure(0,weight=3)
        row.grid_columnconfigure(1,weight=2)

        self.category_parent = row

        self.category_bar = ChartCanvas(
            row,
            build_category_bar_figure(
                state.model_metrics
            )
        )

        self.category_bar.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,Spacing.SM)
        )

        self.category_pie = ChartCanvas(
            row,
            build_category_pie_figure(
                state.model_metrics
            )
        )

        self.category_pie.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(Spacing.SM,0)
        )

    def _build_top_articles_section(self, parent):

        card = Card(
            parent,
            title="5. Top 20 Articles",
            subtitle="Highest semantic similarity scores.",
            icon=Icon.DATASET,
        )

        card.pack(
            fill="x",
            pady=(0,Spacing.LG)
        )

        self.top_articles_parent = card.body

        self.top_articles_table = DataTable(

            card.body,

            TOP_ARTICLES_COLUMNS,

            _build_top_articles_rows(state.model_metrics),

            height=10

        )

        self.top_articles_table.pack(
            fill="both",
            expand=True
        )

    def _build_pca_section(self, parent):
        card = Card(
            parent,
            title="6. Embeddings in 2D",
            subtitle="PCA projection of the 384-dimensional embeddings, colored by category.",
            icon=Icon.AI,
        )
        card.pack(fill="x", pady=(0, Spacing.LG))
        self.pca_parent = card.body

        self.pca_chart = ChartCanvas(
            self.pca_parent,
            build_pca_scatter_figure(state.model_metrics)
        )

        self.pca_chart.pack(
            fill="both",    
            expand=True
        )

        code_row = ctk.CTkFrame(card.body, fg_color=Color.BG_INPUT, corner_radius=Radius.SM,
                                 border_width=1, border_color=Color.BORDER)
        code_row.pack(fill="x", pady=(Spacing.SM, 0))
        ctk.CTkLabel(
            code_row, text="  PCA(n_components=2)   —  alternative: TSNE()",
            font=Font.mono_small(), text_color=Color.SUCCESS, anchor="w"
        ).pack(fill="x", padx=Spacing.SM, pady=6)

    def _build_heatmap_section(self, parent):
        card = Card(
            parent,
            title="7. Similarity Heatmap",
            subtitle="Pairwise cosine similarity among the top 10 ranked articles.",
            icon=Icon.CHART,
        )
        card.pack(fill="x", pady=(0, Spacing.LG))


        wrapper = ctk.CTkFrame(card.body, fg_color=Color.TRANSPARENT)
        wrapper.pack()

        self.heatmap_parent = wrapper

        self.heatmap_chart = ChartCanvas(
            wrapper,
            build_similarity_heatmap_figure(
                state.model_metrics
            )
        )

        self.heatmap_chart.pack()

    def _build_keywords_section(self, parent):
        card = Card(
            parent,
            title="8. Top Keywords",
            subtitle="Most frequent terms across articles marked as Relevant or Highly Relevant.",
            icon=Icon.RECOMMEND,
        )
        card.pack(fill="x", pady=(0, Spacing.LG))

        self.keyword_parent = card.body

        self.keyword_chart = ChartCanvas(

            self.keyword_parent,

            build_keywords_bar_figure(
                state.model_metrics
            )

        )

        self.keyword_chart.pack(
            fill="both",
            expand=True
        )

    def _build_threshold_section(self, parent):
        card = Card(
            parent,
            title="9. Model Thresholds",
            subtitle="Similarity ranges that determine why an article lands in each category.",
            icon=Icon.SETTINGS,
        )
        card.pack(fill="x", pady=(0, Spacing.LG))
        ChartCanvas(card.body, build_threshold_bar_figure()).pack(fill="both", expand=True)

    def _build_metrics_section(self, parent):
        card = Card(
            parent,
            title="10. Model Metrics",
            subtitle="Configuration of the pre-trained embedding model used for scoring.",
            icon=Icon.MODEL,
        )
        card.pack(fill="x", pady=(0, Spacing.LG))

        grid = ctk.CTkFrame(card.body, fg_color=Color.TRANSPARENT)
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="metrics")

        tiles = [
            ("Embedding Model", "BAAI/bge-small-en-v1.5", Color.PRIMARY),
            ("Dimensions", "384", Color.TEXT_PRIMARY),
            ("Normalization", f"{Icon.CHECK} Enabled", Color.SUCCESS),
            ("Similarity Metric", "Cosine Similarity", Color.TEXT_PRIMARY),
            ("Framework", "Sentence Transformers", Color.TEXT_PRIMARY),
            ("Total Articles", "134", Color.PRIMARY),
            ("Average Similarity", "0.57", Color.WARNING),
            ("Highest Similarity", "0.91", Color.SUCCESS),
            ("Lowest Similarity", "0.19", Color.DANGER),
        ]
        for i, (label, value, accent) in enumerate(tiles):
            row, col = divmod(i, 3)
            InfoTile(grid, label, value, accent=accent).grid(
                row=row, column=col, sticky="nsew", padx=6, pady=6
            )

    def _build_confusion_matrix_note(self, parent):
        card = Card(parent, icon=Icon.SETTINGS)
        card.pack(fill="x", pady=(0, Spacing.LG))

        body = card.body
        header_row = ctk.CTkFrame(body, fg_color=Color.TRANSPARENT)
        header_row.pack(fill="x")
        ctk.CTkLabel(
            header_row, text=f"{Icon.DOT} Por qué no hay matriz de confusión",
            font=Font.h3(), text_color=Color.WARNING, anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            body,
            text=(
                "Una matriz de confusión solo tiene sentido cuando existe una verdad base etiquetada "
                "para comparar las predicciones. SearchAI actualmente asigna categorías directamente "
                "desde la puntuación de similitud, sin datos etiquetados manualmente. Mostrar una matriz "
                "de confusión aquí sería artificial y podría generar preguntas sobre qué conjunto de datos "
                "se utilizó como verdad base. Esto se puede agregar más tarde si un conjunto de evaluación "
                "etiquetado está disponible."
            ),
            font=Font.body(), text_color=Color.TEXT_SECONDARY, anchor="w",
            justify="left", wraplength=1180,
        ).pack(fill="x", pady=(6, 0))

    def refresh(self):

        if state.model_metrics is None:
            return

        self._reload_metric_tiles()
        self._reload_evaluation_tiles()
        self._reload_histogram()
        self._reload_category_charts()
        self._reload_top_articles()
        self._reload_pca()
        self._reload_heatmap()
        self._reload_keywords()


    def _reload_heatmap(self):

        self.heatmap_chart.destroy()

        self.heatmap_chart = ChartCanvas(

            self.heatmap_parent,

            build_similarity_heatmap_figure(
                state.model_metrics
            )

        )

        self.heatmap_chart.pack()

    def _reload_pca(self):

        self.pca_chart.destroy()

        self.pca_chart = ChartCanvas(

            self.pca_parent,

            build_pca_scatter_figure(
                state.model_metrics
            )

        )

        self.pca_chart.pack(
            fill="both",
            expand=True
        )

    def _reload_keywords(self):

        self.keyword_chart.destroy()

        self.keyword_chart = ChartCanvas(

            self.keyword_parent,

            build_keywords_bar_figure(
                state.model_metrics
            )

        )

        self.keyword_chart.pack(
            fill="both",
            expand=True
        )

    def _reload_top_articles(self):

        self.top_articles_table.destroy()

        self.top_articles_table = DataTable(

            self.top_articles_parent,

            TOP_ARTICLES_COLUMNS,

            _build_top_articles_rows(state.model_metrics),

            height=10

        )

        self.top_articles_table.pack(
            fill="both",
            expand=True
        )

    def _reload_category_charts(self):

        self.category_bar.destroy()
        self.category_pie.destroy()

        self.category_bar = ChartCanvas(
            self.category_parent,
            build_category_bar_figure(
                state.model_metrics
            )
        )

        self.category_bar.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,Spacing.SM)
        )

        self.category_pie = ChartCanvas(
            self.category_parent,
            build_category_pie_figure(
                state.model_metrics
            )
        )

        self.category_pie.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(Spacing.SM,0)
        )
