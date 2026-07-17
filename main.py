"""
main.py
SearchAI — AI Assistant for Systematic Literature Reviews.

Application entry point. Wires together the sidebar, header, the
swappable view container and the bottom console into a single window.

NOTE: This file (and the whole project) contains UI ONLY.
No search / AI / dataset logic has been implemented — every button and
field is ready to be connected to real backend logic later.
"""

import customtkinter as ctk

from styles.theme import Color
from components.sidebar import Sidebar
from components.header import Header
from components.console import Console

from views.dashboard_view import DashboardView
from views.search_equation_view import SearchEquationView
from views.dataset_view import DatasetView
from views.ai_analysis_view import AIAnalysisView
from views.recommendations_view import RecommendationsView
from views.history_view import HistoryView
from views.ai_model_evaluation_view import AIModelEvaluationView

from services.console_service import console

VIEW_META = {
    "dashboard": ("Research Context", "Define the scope, objectives and notes for your review."),
    "search_equation": ("Search Equation", "Build and validate the boolean search query."),
    "dataset": ("Dataset", "Import and manage the retrieved article corpus."),
    "ai_analysis": ("AI Analysis", "Review AI-generated relevance scoring for your dataset."),
    "recommendations": ("Recommendations", "AI-generated suggestions to refine your equation."),
    "history": ("Iteration History", "Track how your search equation evolved over time."),
}


class SearchAIApp(ctk.CTk):
    """Root application window."""

    def __init__(self):
        super().__init__()

        self.title("SearchAI — AI Assistant for Systematic Literature Reviews")
        self.geometry("1500x900")
        self.minsize(1200, 750)
        self.configure(fg_color=Color.BG_MAIN)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._build_layout()
        self._register_views()
        self.show_view("dashboard")
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.destroy()

    # ------------------------------------------------------------------
    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, on_navigate=self.show_view)
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        # Main column: header (top) + view container (middle) + console (bottom)
        self.main_column = ctk.CTkFrame(self, fg_color=Color.BG_MAIN, corner_radius=0)
        self.main_column.grid(row=0, column=1, sticky="nsew")
        self.main_column.grid_columnconfigure(0, weight=1)
        self.main_column.grid_rowconfigure(1, weight=1)

        self.header = Header(self.main_column)
        self.header.grid(row=0, column=0, sticky="ew")

        self.view_container = ctk.CTkFrame(self.main_column, fg_color=Color.BG_MAIN, corner_radius=0)
        self.view_container.grid(row=1, column=0, sticky="nsew")
        self.view_container.grid_columnconfigure(0, weight=1)
        self.view_container.grid_rowconfigure(0, weight=1)

        self.console = Console(self.main_column)
        self.console.grid(row=2, column=0, sticky="ew")

        console.bind(self.console)

        print(console)
        print(console.console)

    # ------------------------------------------------------------------
    def _register_views(self):
        """Instantiate every view once and stack them (classic multi-page pattern)."""
        self.views = {
            "dashboard": DashboardView(self.view_container),
            "search_equation": SearchEquationView(self.view_container),
            "dataset": DatasetView(self.view_container),
            "ai_analysis": AIAnalysisView(self.view_container),
            "recommendations": RecommendationsView(self.view_container),
            "history": HistoryView(self.view_container),
            "ai_model_evaluation": AIModelEvaluationView(self.view_container),
        }
        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")

    # ------------------------------------------------------------------
    def show_view(self, key):
        """Raise the requested view, update header text and sidebar highlight."""
        if key not in self.views:
            return
        self.views[key].tkraise()
        self.sidebar.set_active(key)

        title, subtitle = VIEW_META.get(key, ("SearchAI", ""))
        self.header.set_title(title, subtitle)


if __name__ == "__main__":
    app = SearchAIApp()
    app.mainloop()
