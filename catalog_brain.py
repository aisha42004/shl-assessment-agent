import json
import re


class CatalogBrain:

    def __init__(self):

        self.catalog_path = "data/shl_catalog.json"

        self.assessments = []

        self.load_catalog()

    # ---------------------------------
    # Clean invalid control characters
    # ---------------------------------

    def clean_json_text(
        self,
        text
    ):

        # remove problematic control chars
        text = re.sub(
            r'[\x00-\x1F\x7F]',
            '',
            text
        )

        return text

    # ---------------------------------
    # Load catalog safely
    # ---------------------------------

    def load_catalog(self):

        with open(
            self.catalog_path,
            "r",
            encoding="utf-8"
        ) as f:

            raw_text = f.read()

        cleaned_text = self.clean_json_text(
            raw_text
        )

        raw_data = json.loads(
            cleaned_text
        )

        cleaned = []

        for item in raw_data:

            assessment = {

                # ---------------------------------
                # Core fields
                # ---------------------------------

                "name":
                item.get("name", ""),

                "description":
                item.get("description", ""),

                "test_type":
                item.get("test_type", ""),

                # ---------------------------------
                # URL handling
                # ---------------------------------

                "url":
                (
                    item.get("url")
                    or item.get("product_url")
                    or item.get("link")
                    or item.get("catalog_url")
                    or ""
                ),

                # ---------------------------------
                # Metadata
                # ---------------------------------

                "job_levels_raw":
                item.get("job_levels_raw", ""),

                "keys":
                item.get("keys", []),

                "languages":
                item.get("languages", []),

                "duration":
                item.get("duration", "")
            }

            cleaned.append(
                assessment
            )

        self.assessments = cleaned

    # ---------------------------------
    # Get all assessments
    # ---------------------------------

    def get_all_assessments(self):

        return self.assessments

    # ---------------------------------
    # Find assessment by name
    # ---------------------------------

    def find_assessment_by_name(
        self,
        query
    ):

        query = query.lower()

        for item in self.assessments:

            name = item.get(
                "name",
                ""
            ).lower()

            if query in name:

                return item

        return None


# ---------------------------------
# Debug
# ---------------------------------

if __name__ == "__main__":

    brain = CatalogBrain()

    data = brain.get_all_assessments()

    print(data[0])