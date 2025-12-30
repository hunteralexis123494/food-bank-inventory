import csv
from item import Item
from measurements import format_unit

class Inventory:
    def __init__(self):
        # A dictionary of items
        self.items = {}
        # Current file inventory is saved as (by deafult is None)
        self.current_file:str | None = None
        # Tracks unsaved changes
        self.changed = False

    # Inventory Management

    # Makes a key based on name, container, food_group, and size
    def make_key(self, name, container, food_group, weight):
        """Makes a key based on the components of the item"""
        return (name.lower(), container.lower(), food_group.lower(), weight.lower())

    # Change Tracking

    # Sets current file
    def set_current_file(self, filename:str):
        """Sets the current file to filename"""
        self.current_file = filename

    # Returns current file value (str)
    def get_current_file(self):
        """Returns the changed flag (True or False)"""
        return self.current_file
    
    # Sets changed flag based on boolean value (True or False)
    def set_changed(self, value:bool):
        """Sets the changed flag to True or False"""
        self.changed = value

    # Returns changed flag boolean value (True or False)
    def get_changed(self):
        """Returns the changed flag (True or False)"""
        return self.changed

    # Add item to inventory
    def add_item(self, name, container, food_group, weight, quantity):
        """
            Adds items to inventory
            Checks if the item is in the inventory
            Makes sure the user isn't trying to remove more than there is in the inventory
            Deletes the item from inventory if there isn't any more of the item (quantity = 0)
        """
        # Compound key (tuple) to check if item added is already in inventory
        # Checks by name, category, and size
        key = self.make_key(name, container, food_group, weight)
        
        # If it's the same item (name, category, size), add to the quantity
        if key in self.items:
            self.items[key].quantity += quantity
        # Otherwise, add the new item to the inventory
        else:
            self.items[key] = Item(name, container, food_group, weight, quantity)

        # Reflects that a change has been made to inventory
        self.set_changed(True)

    # Remove item from inventory
    def remove_item(self, name, container, food_group, weight, quantity):
        """
            Removes items from inventory
            Checks if the item is in the inventory
            Makes sure the user isn't trying to remove more than there is in the inventory
            Deletes the item from inventory if there isn't any more of the item (quantity = 0)
        """
        
        key = self.make_key(name, container, food_group, weight)

        # If item is in inventory, subtract from the quantity
        if key in self.items:
            # If user tries to remove a valid quantity (not asking for more than available), remove that amount
            if quantity <= self.items[key].quantity:
                self.items[key].quantity -= quantity
            # Otherwise, print error message and exit
            else:
                print(f"Cannot remove {quantity}. Only {self.items[key].quantity} available.")
                return

            # If the quantity is <= 0, the item has run out and is removed from the inventory (items dictionary)
            if self.items[key].quantity <= 0:
                del self.items[key]

            # Reflects that a change has been made to inventory
            self.set_changed(True)

    # Returns a list of item values in inventory
    def get_all_items(self):
        """Return a list of all Items values in inventory"""
        return list(self.items.values())

    # Returns the total quantity of items in inventory
    def get_total_quantity(self) -> int:
        """Return the total quantity of all items in inventory"""
        # Setting initial value to 0
        total = 0
        # Iterating through each item in inventory
        for item in self.items.values():
            # Adding quantity of each item to total
            total += item.quantity
        return total

    # Returns the total number of unique items in inventory
    def get_total_unique_items(self) -> int:
        """Return the total number of unique items in inventory"""
        return len(self.items)

    # Display function

    # Displays all items in Inventory
    def display_inventory(self):
        """Displays all items fromt the current inventory"""
        # Prints newline
        print()
        
        # If inventory is empty, print message and return to menu
        if not self.items:
            print("Inventory is empty.")
            return

        # Copy inventory items to temp local variable
        all_items = self.get_all_items()

        # Print each item from inventory
        for item in all_items:
            formatted_weight = format_unit(item.weight)
            print(f"{item.name.title()} ({formatted_weight}, {item.container.title()}, {item.food_group.title()}) - Qty: {item.quantity}")

    # Displays total values (unique items and total quantity)
    def display_totals(self):
        """Prints total values (unique items and total quantity)"""
        # Stores total quantity and total unique items to variables
        total_quantity = self.get_total_quantity()
        total_unique_items = self.get_total_unique_items()

        #Prints totals
        print(f"Total unique items: {total_unique_items}")
        print(f"Total quantity: {total_quantity}\n")

    # CSV Functions

    # Load inventory from csv file
    def load_inventory_from_csv(self, filename):
        """Load items from a CSV file to the inventory"""
        # Try to read the csv file
        try:
            # Open the CSV file for reading with UTF-8 encoding.
            # 'newline=""' ensures consistent line endings across OSes.
            # Using 'with' automatically closes the file when done.
            with open(filename, 'r', newline='', encoding='utf-8') as file:
                # Create a CSV DictReader to read each row as a dictionary
                reader = csv.DictReader(file)

                # Clear current items in inventory
                self.items.clear()

                # Iterate through each row
                for row in reader:
                    # Store data from the row to variables
                    name = row["name"]
                    container = row["container"]
                    food_group = row["food_group"]
                    weight = row["weight"]
                    quantity = int(row["quantity"])

                    # Add item to inventory
                    self.add_item(name, container, food_group, weight, quantity)

                # Ensures that the inventory changed flag stays False since loading doesn't count as a change
                # load function calls on add_item function in inventory, which makes changed flag true
                self.set_changed(False)

                # Sets current file to filename
                self.set_current_file(filename)

                # Print confirmation message that inventory loaded successfully from csv file
                print(f"\nInventory loaded from '{filename}'.\n")

        # CSV file does not exist or is not found in directory
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found.")
        # CSV file exists but has invalid format
        except csv.Error as e:
            raise ValueError(F"Malformed CSV: {e}")
        # Any other unexpected errors (permissions, I/O, etc.)
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}")

    # Saves the inventory data to a CSV file
    def save_inventory_to_csv(self, filename):
        """
            Saves the current inventory data to a csv file

            CSV file will have the following information on each row:
            name, container, food_group, weight, and quantity

            If the inventory is empty, a message is printed and no file is created
        """

        # Check if the inventory is empty
        if not self.items:
            print("\nInventory is empty. Nothing to save.\n")
            return

        # Open the CSV file for writing
        # 'newline=""' ensures consistent line endings for the csv module
        # 'encoding="utf-8"' allows special characters in item names
        # 'with' ensures the file is automatically closed when done
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            # Define the column headers for the csv file
            fieldnames = ["name", "container", "food_group", "weight", "quantity"]

            # Create a DictWriter to write dictionaries as rows in the CSV file
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Loop through all items in the inventory
            for item in self.get_all_items():
                # Write each item as a row in the CSV file
                writer.writerow({
                    "name": item.name,
                    "container": item.container,
                    "food_group": item.food_group,
                    "weight": item.weight,
                    "quantity": item.quantity    
                })

            # Print confirmation message
            print(f"\nInventory saved to '{filename}'. Make sure to check the file in the same directory.")

            # Reflects that changes have been saved, so the changed flag gets reset to False
            self.set_changed(False)

    # Returns a sorted list of items based on input
    def get_sorted_items(self, sort_by: str = "name", reverse: bool = False):
        """
            Returns a list of sorted items by the given attributes
            sort_by can be "name", "container", "food_group", "weight", or "quantity"
            Default: sort by "name" (alphabetical order)
            reverse: True = descending order, False = ascending order
        """
        # Dictionary of keys that refer to what the program can sort by
        valid_keys = {"name", "container", "food_group", "weight", "quantity"}

        # Validate sort_by
        if sort_by not in valid_keys:
            sort_by = "name"

        # Sort the items
        return sorted(
            # Get all items in inventory
            self.get_all_items(),
            # Sort by the attribute chosen in sort_by (name, container, food_group, etc.)
            key=lambda item: getattr(item, sort_by),
            # Set reverse to input (True = descending order, False = ascending order)
            reverse = reverse
        )