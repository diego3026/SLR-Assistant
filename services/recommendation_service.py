import re
from collections import Counter
from sentence_transformers import SentenceTransformer
from services.console_service import console

class RecommendationService:
    def __init__(self):
        self.embedding_model = None

    def normalize_equation(self, equation):
        equation = equation.lower()
        equation = re.sub(
            r'[\(\)]',
            '',
            equation
        )

        equation = equation.replace(
            '"',
            ''
        )

        equation = equation.replace(
            "AND",
            " "
        )

        equation = equation.replace(
            "OR",
            " "
        )

        tokens = [
            x.strip()
            for x in equation.split()
            if len(x.strip()) > 2
        ]

        return set(tokens)

    def get_relevant_articles(self, dataframe):

        relevant = dataframe[
            dataframe["Category"].isin(
                [
                    "Highly Relevant",
                    "Relevant"
                ]
            )
        ]
        return relevant

    def generate_recommendations(
        self,
        dataframe,
        equation,
        context_embedding,
        embedding_model
    ):
        console.info("Generating search recommendations...")

        self.embedding_model = embedding_model

        relevant = dataframe[
            dataframe["Category"].isin(
                [
                    "Highly Relevant",
                    "Relevant"
                ]
            )
        ]

        if relevant.empty:
            console.warning(
                "No relevant articles found. Recommendation step skipped."
            )
            return []

        keywords = []

        for value in relevant["Author Keywords"].dropna():

            for term in str(value).split(";"):

                term = term.strip().lower()

                if len(term) > 2:
                    keywords.append(term)

        counts = Counter(keywords)

        console.info(
            f"Found {len(counts)} candidate keywords."
        )

        equation_lower = equation.lower()

        # Eliminar términos que ya están en la ecuación
        terms = [
            term
            for term in counts.keys()
            if term not in equation_lower
        ]

        if not terms:
            console.warning(
                "No new keywords available for recommendation."
            )
            return []

        console.info(
            "Computing semantic relevance for candidate terms..."
        )

        embeddings = self.embedding_model.encode(
            terms,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        candidates = []

        for term, emb in zip(terms, embeddings):

            freq = counts[term]

            similarity = float(
                emb @ context_embedding
            )

            score = (
                similarity * 0.8 +
                min(freq / 10, 1.0) * 0.2
            )

            if score >= 0.75:
                priority = "High"
            elif score >= 0.60:
                priority = "Medium"
            else:
                priority = "Low"

            reason = (
                f'Encontrado en {freq} artículos relevantes '
                f'con una similitud semántica de {similarity:.2f}.'
            )

            candidates.append(
                {
                    "action": "add",
                    "term": term,
                    "frequency": freq,
                    "similarity": similarity,
                    "score": score,
                    "priority": priority,
                    "reason": reason
                }
            )

        candidates.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        console.success(
            f"{len(candidates[:15])} recommendations generated."
        )

        return candidates[:15]

    def build_new_equation(
        self,
        current_equation,
        recommendations,
        max_terms=5
    ):
        console.info("Building optimized search equation...")

        additions = []

        for item in recommendations[:max_terms]:
            additions.append(
                f'"{item["term"]}"'
            )

        if len(additions)==0:
            console.warning(
                "No recommendations available. Original equation kept."
            )
            return current_equation

        block = "\nOR\n".join(additions)

        console.success(
            f"Added {len(additions)} suggested terms."
        )
        
        return (
            f"{current_equation}\n\n"
            f"AND\n"
            f"(\n"
            f"  {block}\n"
            f")"
        )