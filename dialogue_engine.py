class DialogueEngine:

    def __init__(self):

        self.out_of_scope_words = [
            "weather",
            "politics",
            "lawsuit",
            "medical",
            "religion"
        ]

        self.injection_patterns = [
            "ignore previous instructions",
            "reveal system prompt",
            "jailbreak",
            "bypass"
        ]

    # ---------------------------------
    # Prompt Injection
    # ---------------------------------

    def is_prompt_injection(self, text):

        text = text.lower()

        return any(
            pattern in text
            for pattern in self.injection_patterns
        )

    # ---------------------------------
    # Out-of-scope
    # ---------------------------------

    def is_out_of_scope(self, text):

        text = text.lower()

        return any(
            word in text
            for word in self.out_of_scope_words
        )

    # ---------------------------------
    # Comparison Detection
    # ---------------------------------

    def is_comparison_request(self, text):

        text = text.lower()

        triggers = [
            "compare",
            "difference",
            "vs",
            "versus"
        ]

        return any(
            trigger in text
            for trigger in triggers
        )

    # ---------------------------------
    # Extract Comparison Items
    # ---------------------------------

    def extract_comparison_items(self, text):

        text = text.lower().strip()

        text = text.replace("compare", "")
        text = text.replace("difference between", "")
        text = text.replace("versus", "vs")

        if "vs" in text:

            parts = text.split("vs")

            if len(parts) >= 2:

                left = parts[0].strip()

                right = parts[1].strip()

                return left, right

        return None, None

    # ---------------------------------
    # Clarification Decision
    # ---------------------------------

    def needs_clarification(
        self,
        user_text
    ):

        text = user_text.lower().strip()

        vague_inputs = [
            "assessment",
            "need assessment",
            "i need an assessment",
            "recommend assessment",
            "test"
        ]

        if text in vague_inputs:

            return True

        if len(text.split()) <= 2:

            return True

        return False