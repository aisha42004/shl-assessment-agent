from catalog_brain import CatalogBrain

brain = CatalogBrain()

all_items = brain.get_all_assessments()

print("TOTAL:", len(all_items))

print("\nFIRST CLEAN ITEM:\n")

print(all_items[0])