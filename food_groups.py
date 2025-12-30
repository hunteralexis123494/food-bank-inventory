from typing import Optional

"""
    This variation map allows for various user input to be mapped to the
    correct food group label
"""

VARIATION_FOOD_GROUP_MAP = {
    # Grains
    "grains": "Grains",
    "grain": "Grains",

    "cereal": "Grains",
    "bread": "Grains",
    

    # Vegetables
    "vegetables": "Vegetables",
    "vegetable": "Vegetables",
    
    "veg": "Vegetables",
    "veggie": "Vegetables",
    "veggies": "Vegetables",

    # Fruits
    "fruits": "Fruits",
    "fruit": "Fruits",

    # Protein
    "protein": "Protein",
    "proteins": "Protein",

    # Dairy
    "dairy": "Dairy",
    "dairies": "Dairy",

    # Fats/Oils
    "fats/oils": "Fats/Oils",
    "fat/oil": "Fats/Oils",
    "fats": "Fats/Oils",
    "fat": "Fats/Oils",
    "oils": "Fats/Oils",
    "oil": "Fats/Oils",

    # Beverages
    "beverages": "Beverages",
    "beverage": "Beverages",
    "bev": "Beverages",
    "bevs": "Beverages",

    # Snacks/Other
    "snacks/other": "Snacks/Other",
    "snacks/others": "Snacks/Other",
    "snacks": "Snacks/Other",
    "snack": "Snacks/Other",
    "other": "Snacks/Other",
    "others": "Snacks/Other",
}

# Sorted list of food groups (no duplicates, alphabetical order)
CANONICAL_FOOD_GROUPS = sorted(set(VARIATION_FOOD_GROUP_MAP.values()))

# Normalizes input of food group
def normalize_food_group(value: str) -> Optional[str]:
    """
        Normalizes user input to a canonical food group
        If user input is recognized, return the canonical food group
        Otherwise, return None
    """
    # Return None if empty string
    if not value:
        return None

    # Return either recognized canonical food group or None depending on user input
    return VARIATION_FOOD_GROUP_MAP.get(value.strip().lower())
