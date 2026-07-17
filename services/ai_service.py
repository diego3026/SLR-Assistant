from pathlib import Path

import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from services.console_service import console

SIMILARITY_THRESHOLD = 0.50

class AIService:
    """
    SearchAI AI Engine

    Pipeline

    CSV
        ↓
    Text construction
        ↓
    Embeddings (BGE)
        ↓
    Cosine Similarity
        ↓
    Ranking
        ↓
    Classification
    """

    def __init__(self):

        self.model = None
        self.dataset = None

        self.context_embedding = None
        self.article_embeddings = None
        
    def log(self, message, level="info"):
        if self.console:
            self.console.append(message, level)
        else:
            print(message)

    def load_model(self):
        
        if self.model is None:

            console.info("Loading embedding model (BAAI/bge-small-en-v1.5)...")

            self.model = SentenceTransformer(
                "BAAI/bge-small-en-v1.5"
            )

            console.success("Embedding model loaded.")

    def load_dataset(self, csv_path):

        console.info(f"Loading dataset: {Path(csv_path).name}")

        df = pd.read_csv(csv_path)

        required = [
            "Title",
            "Abstract",
            "Author Keywords"
        ]

        for col in required:
            if col not in df.columns:
                df[col] = ""

        df.fillna("", inplace=True)

        df["Document"] = (
            df["Title"]
            + " "
            + df["Abstract"]
            + " "
            + df["Author Keywords"]
        )
        self.dataset = df

        console.success(
            f"Dataset loaded successfully ({len(df)} articles)."
        )

        return df


    def build_context(
        self,
        topic,
        objectives="",
        notes=""
    ):
        context = f"""

        Research Topic:
        {topic}

        Objectives:
        {objectives}

        Notes:
        {notes}

        """
        return context.strip()

    def classify_score(self, score):
        if score >= 0.65:
            return "Highly Relevant"

        elif score >= SIMILARITY_THRESHOLD:
            return "Relevant"

        elif score >= 0.35:
            return "Low Relevance"

        return "Noise"

    def analyze(
        self,
        topic,
        objectives="",
        notes=""
    ):
        console.info("Starting semantic analysis...")

        self.load_model()

        console.info("Building research context...")

        context = self.build_context(
            topic,
            objectives,
            notes
        )

        console.info("Generating context embedding...")
        

        self.context_embedding = self.model.encode(
            context,
            normalize_embeddings=True
        )

        console.success("Context embedding generated.")

        article_embeddings = self.model.encode(
            self.dataset["Document"].tolist(),
            normalize_embeddings=True,
            show_progress_bar=True
        )

        self.article_embeddings = article_embeddings

        console.success("Article embeddings generated.")

        console.info("Computing cosine similarity...")

        scores = cosine_similarity(
            [self.context_embedding],
            article_embeddings
        )[0]

        self.dataset["Similarity"] = scores

        self.dataset["Similarity"] = (
            self.dataset["Similarity"]
            .round(4)
        )

        self.dataset["Category"] = (
            self.dataset["Similarity"]
            .apply(self.classify_score)
        )

        self.dataset.sort_values(
            by="Similarity",
            ascending=False,
            inplace=True
        )

        self.dataset.reset_index(
            drop=True,
            inplace=True
        )

        high = (self.dataset["Category"]=="Highly Relevant").sum()
        rel = (self.dataset["Category"]=="Relevant").sum()

        console.success(
            f"Analysis finished: {high} highly relevant, {rel} relevant articles."
        )

        console.success(
            "Semantic ranking completed."
        )

        return self.dataset

    def get_results(self):
        return self.dataset