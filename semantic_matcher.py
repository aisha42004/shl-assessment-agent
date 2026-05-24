from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SemanticMatcher:

    def __init__(self, assessments):

        self.assessments = assessments

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.search_texts = []

        for item in assessments:

            combined_text = f"""
            {item['name']}
            {item['description']}
            {' '.join(item['job_levels'])}
            {' '.join(item['keys'])}
            """

            self.search_texts.append(combined_text)

        print("Creating embeddings...")

        self.embeddings = self.model.encode(
            self.search_texts,
            convert_to_numpy=True
        )

        print("Semantic engine ready.")

    def search(self, query, top_k=5):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        similarity_scores = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]

        best_indexes = np.argsort(
            similarity_scores
        )[::-1][:top_k]

        results = []

        for idx in best_indexes:

            results.append(
                self.assessments[idx]
            )

        return results