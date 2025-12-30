import re

# Valid units for item weight and volume
UNIT_MAP = {
    # Ounces
    "oz": "oz",
    "ounce": "oz",
    "ounces": "oz",

    # Fluid ounces
    "fl oz": "fl oz",
    "floz": "fl oz",
    "fl. oz": "fl oz",

    # Pounds
    "lb": "lb",
    "lbs": "lb",
    "pound": "lb",
    "pounds": "lb",

    # Grams
    "kg": "kg",
    "kilogram": "kg",
    "kilograms": "kg",

    # Milliliters
    "ml": "mL",
    "milliliter": "mL",
    "milliliters": "mL",
    "millilitre": "mL",
    "millilitres": "mL",

    # Liters
    "l": "L",
    "liter": "L",
    "liters": "L",
    "litre": "L",
    "litres": "L"
}

# Format unit according to the valid units and return a string
def format_unit(value: str) -> str:
    """
    Formats units for standardized units.
    Requires a number AND a valid unit; otherwise raises ValueError.
    Handles extra spaces between number and unit.
    Ex:
        1l --> 1 L
        500 ml --> 500 mL
        2 lbs --> 2 lb
        8   fl oz --> 8 fl oz
    """
    # Remove whitespace before and after value input
    # Removes any commas (typically in numbers; e.g. 1,000 --> 1000)
    value = value.strip().replace(",","")

    # If value is empty, return the empty string
    if not value:
        return value

    # Split number and unit (first numeric part)
    # Must be a number + optional spaces + at least one non-space character
    match = re.match(r"^(\d+(?:\.\d+)?)(.*)$", value)

    # If the unit does not match a valid unit, raise ValueError (must be number and unit)
    if not match:
        raise ValueError(f"Invalid input '{value}'. Must include a number and a unit.")

    # Separate number and unit
    number_part = match.group(1)
    unit_part = match.group(2).strip().lower()

    # Automatically insert space if missing and normalize multiple spaces
    unit_part = " ".join(unit_part.split())

     # If not found, raise ValueError (invalid unit)
    if unit_part not in UNIT_MAP:
        raise ValueError(f"Invalid unit '{unit_part}'.")

    # Look up in UNIT_MAP
    normalized_unit = UNIT_MAP[unit_part]

    # Return number and unit together in one string
    return f"{number_part} {normalized_unit}"