from catalog_brain import CatalogBrain
from semantic_matcher import SemanticMatcher

brain = CatalogBrain()

all_items = brain.get_all_assessments()

matcher = SemanticMatcher(all_items)

results = matcher.search(
    "Java developer with stakeholder communication",
    top_k=5
)

for item in results:

    print("\n-------------------")

    print("NAME:", item["name"])

    print("URL:", item["url"])

    print("KEYS:", item["keys"])