from menu_manager import MenuManager
from inventory import Inventory
from config import load_config

def main():
    """
        Program entry point
        - Loads config
        - Creates Inventory
        - Loads CSV file if available
        - Starts MenuManager main menu loop
    """

    # Load configuration
    # Stores food bank name and inventory csv from config.txt
    food_bank_name, inventory_csv = load_config()

    # Create inventory instance
    inventory = Inventory()

    # If the name is an empty string, print the error message and prompt user for food bank name
    if not food_bank_name:
        print("Could not load food bank name from config.\n")

        # Keeps asking user for name until user gives valid input
        while True:
            food_bank_name = input("Enter the name of your food bank: ").strip()

            # If user gives input, continue to the next step (break from loop)
            if food_bank_name:
                break
            # If user does not enter anything, print error message
            print("\nName cannot be empty.\n")

    # Attempt to load inventory CSV if provided
    # Prints error messages if unsuccessful and starts with empty inventory
    if inventory_csv:
        try:
            inventory.load_inventory_from_csv(inventory_csv)
        # CSV file does not exist or is not found in directory
        except FileNotFoundError:
            print(f"Inventory file '{inventory_csv}' not found. Starting with an empty inventory.\n")
        # CSV file exists but has invalid format
        except ValueError as ve:
            print(f"Error: {ve}. Starting with an empty inventory.\n")
        # Any other unexpected errors (permissions, I/O, etc.)
        except RuntimeError as re:
            print(f"Unexpected error loading inventory: {re}. Starting with an empty inventory.\n")
    # Otherwise, print error message and indicate that it will start with an empty inventory
    else:
        print("No inventory file found in config. Starting with an empty inventory.\n")

    # Pass inventory and food bank name in menu manager
    menu = MenuManager(inventory, food_bank_name)

    # Run the main menu loop
    menu.main_menu()

# Only run main when executing this program
if __name__ == "__main__":
    main()
