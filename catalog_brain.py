import json
import re


class CatalogBrain:

    def __init__(self):

        with open(
            "data/shl_catalog.json",
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            raw_text = file.read()

        cleaned_text = re.sub(
            r'[\x00-\x1F\x7F]',
            '',
            raw_text
        )

        raw_data = json.loads(cleaned_text)

        self.assessments = []

        for item in raw_data:

            assessment = {
                "name": item.get("name", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
                "job_levels": item.get("job_levels", []),
                "remote": item.get("remote", ""),
                "adaptive": item.get("adaptive", ""),
                "languages": item.get("languages", []),
                "keys": item.get("keys", []),
                "test_type": self.detect_test_type(item)
            }

            self.assessments.append(assessment)

    # ---------------------------------
    # Detect test type
    # ---------------------------------

    def detect_test_type(self, item):

        text = str(item).lower()

        if "personality" in text:
            return "P"

        if "ability" in text or "aptitude" in text:
            return "A"

        if "technical" in text or "knowledge" in text:
            return "K"

        if "behavior" in text:
            return "B"

        return "General"

    # ---------------------------------
    # Return all assessments
    # ---------------------------------

    def get_all_assessments(self):

        return self.assessments

    # ---------------------------------
    # Smart assessment lookup
    # ---------------------------------

    def find_assessment_by_name(self, query_name):

        query_name = query_name.lower().strip()

        # Hardcoded known abbreviations
        abbreviation_map = {
            "gsa": "global skills assessment",
            "opq": "opq"
        }

        if query_name in abbreviation_map:
            query_name = abbreviation_map[query_name]

        best_match = None

        for item in self.assessments:

            assessment_name = item["name"].lower()

            # Exact containment
            if query_name in assessment_name:
                return item

            # Loose matching
            query_words = query_name.split()

            for word in query_words:

                if len(word) > 2 and word in assessment_name:
                    best_match = item

        return best_match