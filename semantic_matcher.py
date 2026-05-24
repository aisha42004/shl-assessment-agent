from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatcher:

    def __init__(self, assessments):

        self.assessments = assessments

        self.documents = []

        # ---------------------------------
        # Build searchable text
        # ---------------------------------

        for item in assessments:

            text = " ".join([

                item.get("name", ""),
                item.get("description", ""),
                item.get("job_levels_raw", ""),
                item.get("test_type", ""),
                " ".join(item.get("keys", []))

            ])

            self.documents.append(text)

        # ---------------------------------
        # TF-IDF Vectorizer
        # ---------------------------------

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.document_vectors = self.vectorizer.fit_transform(
            self.documents
        )

    # ---------------------------------
    # Search Function
    # ---------------------------------

    def search(
        self,
        query,
        top_k=5
    ):

        query_vector = self.vectorizer.transform(
            [query]
        )

        similarities = cosine_similarity(
            query_vector,
            self.document_vectors
        )[0]

        scored = list(zip(
            self.assessments,
            similarities
        ))

        scored.sort(
            key=lambda x: x[1],
            reverse=True
        )

        results = [
            item[0]
            for item in scored[:top_k]
        ]

        return results