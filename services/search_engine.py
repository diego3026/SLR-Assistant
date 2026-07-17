from services.ai_service import AIService, SIMILARITY_THRESHOLD
from services.recommendation_service import RecommendationService
from services.history_service import HistoryService
from services.console_service import console
from services.app_state import state

class SearchEngine:
    """
    Orquestador principal del proyecto.
    Flujo:
    CSV
        ↓
    AI Analysis
        ↓
    Recommendations
        ↓
    History
        ↓
    Return Results
    """

    def __init__(self):
        self.ai = AIService()
        self.recommendation = RecommendationService()
        self.history = HistoryService()

    def run(self, csv_path, topic, objectives, notes, equation):
        # ---------------------------------------------------------
        # 1. Load Dataset
        # ---------------------------------------------------------
        console.info("Starting SearchAI pipeline...")

        console.info("Step 1/6 - Loading dataset...")

        self.ai.load_dataset(csv_path)

        # ---------------------------------------------------------
        # 2. Analyze Dataset
        # ---------------------------------------------------------

        console.info("Step 2/6 - Running semantic analysis...")

        dataframe = self.ai.analyze(
            topic=topic,
            objectives=objectives,
            notes=notes
        )

        similarities = dataframe["Similarity"].astype(float)

        categories = dataframe["Category"]

        state.model_metrics = {

            "dataset_size": len(dataframe),

            "embedding_model": "BAAI/bge-small-en-v1.5",

            "embedding_size": 384,

            "similarity_metric": "Cosine Similarity",

            "average_similarity": float(similarities.mean()),

            "highest_similarity": float(similarities.max()),

            "lowest_similarity": float(similarities.min()),

            "similarity_threshold": SIMILARITY_THRESHOLD,

            "relevant_articles": int(
                categories.isin(
                    [
                        "Highly Relevant",
                        "Relevant"
                    ]
                ).sum()
            ),

            "discarded_articles": int(
                categories.eq("Noise").sum()
            ),

            "category_counts": categories.value_counts().to_dict(),

            "similarity_scores": similarities.tolist(),

            "dataframe": dataframe.copy(),

            "embeddings": self.ai.article_embeddings
        }

        self.recommendation.embedding_model = self.ai.model

        # ---------------------------------------------------------
        # 3. Recommendations
        # ---------------------------------------------------------

        console.info("Step 3/6 - Generating recommendations...")

        recommendations = self.recommendation.generate_recommendations(
            dataframe,
            equation,
            self.ai.context_embedding,
            self.ai.model
        )

        console.success(
            f"{len(recommendations)} recommendations generated."
        )

        # ---------------------------------------------------------
        # 4. New Equation
        # ---------------------------------------------------------

        console.info("Step 4/6 - Building optimized search equation...")

        new_equation = self.recommendation.build_new_equation(equation, recommendations)

        # ---------------------------------------------------------
        # 5. Statistics
        # ---------------------------------------------------------

        console.info("Step 5/6 - Computing statistics...")

        statistics = self.history.create_statistics(dataframe)

        # ---------------------------------------------------------
        # 6. Save Iteration
        # ---------------------------------------------------------

        console.info("Step 6/6 - Saving iteration history...")

        history_file = self.history.save_iteration(
            topic=topic,
            objectives=objectives,
            notes=notes,
            equation=equation,
            dataframe=dataframe,
            recommendations=recommendations,
            new_equation=new_equation
        )

        # ---------------------------------------------------------
        # 7. Return
        # ---------------------------------------------------------

        console.success("SearchAI pipeline completed successfully.")

        return {
            "dataframe": dataframe,
            "recommendations": recommendations,
            "new_equation": new_equation,
            "statistics": statistics,
            "history_file": history_file
        }