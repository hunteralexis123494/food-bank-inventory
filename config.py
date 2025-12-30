# Loads data from the configuration file
# If no file is provided, uses "config.txt" by default
def load_config(config_path="config.txt"):
    """
        Loads the food bank name and inventory csv from "config.txt"

        Return None for the following cases:
        File not found
        Empty file/empty strings
    """
    food_bank_name = None
    inventory_csv = None

    # Reads from the configure file and creates a list of the text in each line
    # Removes extra whitespace
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]
    # If there's an error, return None for both food bank name and inventory csv
    except FileNotFoundError:
        return (None, None)

    # Creates a new list of non-empty lines from config file
    # Lines don't get added if they are empty strings
    non_empty = [line for line in lines if line]

    # If the file is empty, returns None, which will trigger to ask the user for a name
    if not non_empty:
        return (None, None)

    # For each line in non_empty
    for line in non_empty:
        # If the line starts with "food bank name:", remove "food bank name:" and store what's after
        if line.lower().startswith("food bank name:"):
            food_bank_name = line.split(":", 1)[1].strip()
        # If the line starts with "inventory csv:", remove "inventory csv:" and store what's after
        elif line.lower().startswith("inventory csv:"):
            inventory_csv = line.split(":", 1)[1].strip()

    # If the variables store empty strings, make them store None
    if food_bank_name == "":
        food_bank_name = None
    if inventory_csv == "":
        inventory_csv = None

    return (food_bank_name, inventory_csv)

# Saves the food bank name and inventory csv data to the configuration file
def save_config(food_bank_name, inventory_csv, config_path = "config.txt"):
    """
        Save food bank name and inventory csv to config.txt
        Empty or None value will be written as "" (empty string) 
    """
    # Normalize values
    # Set the values to the input if not empty
    # Otherwise, set it to an empty string
    name_out = food_bank_name.strip() if food_bank_name else ""
    csv_out = inventory_csv.strip() if inventory_csv else ""

    # Write to file the following:
    # Food Bank Name: "food_bank_name"
    # Inventory CSV: "inventory_csv"
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(f"Food Bank Name: {name_out}\n")
            f.write(f"Inventory CSV: {csv_out}")
            print(f"Config saved successfully to {config_path}.\n")
    except Exception as e:
        print(f"Error saving config to {config_path}: {e}")
        print("Be sure input is valid or file is in the same directory.\n")