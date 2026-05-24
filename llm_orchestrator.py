class LLMOrchestrator:

    # ---------------------------------
    # Recommendation Reply
    # ---------------------------------

    def generate_recommendation_reply(
        self,
        user_query,
        recommendations
    ):

        if not recommendations:

            return (
                "No suitable SHL assessments were identified."
            )

        names = [
            item["name"]
            for item in recommendations
        ]

        joined = ", ".join(names[:3])

        return (
            f"Based on the hiring requirements provided, "
            f"the most relevant SHL assessments include "
            f"{joined}. "
            f"These assessments align with the role, "
            f"required competencies, and evaluation goals."
        )

    # ---------------------------------
    # Comparison Reply
    # ---------------------------------

    def generate_comparison_reply(
        self,
        left_item,
        right_item
    ):

        return (
            f"{left_item['name']} focuses on "
            f"{left_item['description']} "
            f"Whereas {right_item['name']} focuses on "
            f"{right_item['description']}"
        )