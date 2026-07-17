from pathlib import Path
from datetime import datetime
from services.console_service import console
import json

class HistoryService:

    def __init__(self):
        self.history_folder = Path("data/history")
        self.history_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    def create_statistics(self, dataframe):
        console.info("Computing analysis statistics...")

        stats = {
            "total_articles": len(dataframe),
            "highly_relevant": len(
                dataframe[
                    dataframe["Category"]=="Highly Relevant"
                ]
            ),
            "relevant": len(
                dataframe[
                    dataframe["Category"]=="Relevant"
                ]
            ),
            "low_relevance": len(
                dataframe[
                    dataframe["Category"]=="Low Relevance"
                ]
            ),
            "noise": len(
                dataframe[
                    dataframe["Category"]=="Noise"
                ]
            ),
            "average_similarity": float(dataframe["Similarity"].mean())
        }

        console.success(
            f"{stats['total_articles']} articles analyzed."
        )

        return {
            "total_articles": stats["total_articles"],
            "highly_relevant": stats["highly_relevant"],
            "relevant": stats["relevant"],
            "noise": stats["noise"],
            "average_similarity": stats["average_similarity"]
        }

    def save_iteration(self, topic, objectives, notes, equation, dataframe, recommendations, new_equation):
        console.info("Saving iteration history...")

        now = datetime.now()

        filename = now.strftime("%Y%m%d_%H%M%S")

        data = {
            "date": now.strftime("%Y-%m-%d %H:%M:%S"),
            "research_topic": topic,
            "objectives": objectives,
            "notes": notes,
            "equation": equation,
            "statistics": self.create_statistics(
                dataframe
            ),
            "recommendations": recommendations,
            "generated_equation": new_equation
        }

        file = self.history_folder / f"{filename}.json"

        with open(
            file,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        console.success(
            f"Iteration saved: {filename}.json"
        )
        return file

    def list_history(self):
        console.info("Loading iteration history...")
        
        files = list(
            self.history_folder.glob("*.json")
        )
        files.sort(reverse=True)
        return files

    def load_history(self, file):
        console.info(
            f"Opening {Path(file).name}"
        )
        with open(
            file,
            encoding="utf8"
        ) as f:

            return json.load(f)