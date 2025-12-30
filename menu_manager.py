import os
from food_groups import VARIATION_FOOD_GROUP_MAP, CANONICAL_FOOD_GROUPS
from measurements import format_unit
from config import save_config

class MenuManager:
    # Valid yes responses for confirmation
    YES_KEYS = ["y", "yes"]
    # Valid no responses for confirmation
    NO_KEYS = ["n", "no"]
    
    def __init__(self, inventory, food_bank_name):
        self.inventory = inventory
        self.food_bank_name = food_bank_name
        # Keeps track of when program will end
        self.end_program = False

    # Draws a border made of *
    def draw_border(self):
        """
            Draws a border (***)
        """
        print("************************************************************")

    # Draws a header with borders around input
    def draw_header_with_borders(self, header):
        """
            Draws borders (***) around the input
        """
        self.draw_border()
        print(header)
        self.draw_border()

    # Confirmation Prompt
    def get_confirmation(self, prompt):
        """
            Get a yes/no confirmation from user before performing an action
            Return True for yes
            Return False for no
            If user inputs invalid response, give error message and ask again
        """
        while True:
            choice = input("\n" + prompt + " (y/n): ").strip().lower()
            if choice in self.YES_KEYS:
                return True
            elif choice in self.NO_KEYS:
                return False
            else:
                print("\nInvalid input. Please enter 'y' or 'n'.")

    # Prints goodbye message
    def print_goodbye(self):
        """Prints goodbye message"""
        print("Goodbye!")

    # Draws main menu
    def print_main_menu(self):
        """Prints the menu (basic GUI)"""

        header = "Welcome to " + self.food_bank_name + " Inventory System!"
        self.draw_header_with_borders(header)
        print()

        print("(1) View Inventory\n")
        print("(2) Add Item to Inventory\n")
        print("(3) Remove Item from Inventory\n")
        print("(4) Load Inventory from CSV File\n")
        print("(5) Save Inventory to CSV File\n")
        print("(Q) Quit\n")

    # Displays display inventory menu
    def display_inventory_menu(self):
        """
            Displays the display inventory menu
            Shows the following options:
            (1) Show Inventory
            (2) Sort Inventory
            (R) Return to Main Menu
        """
        # If inventory is empty, show empty inventory message and return to main menu
        if not self.inventory.items:
            print("\nInventory is empty. Nothing to view.\n")
            return
    
        while True:
            # Prints newline
            print()

            # Puts "VIEW INVENTORY MENU" in borders
            header = "VIEW INVENTORY MENU"
            self.draw_header_with_borders(header)

            # Prints newline
            print()

            # Print menu and record user input
            print("(1) Show Inventory (Default View)")
            print("(2) Sort Inventory")
            print("(R) Return to Main Menu")
            print()
            # Ask user to choose an option
            user_input = input("Choose one of the following options: ").strip().lower()

            # If user presses 1, show inventory
            if user_input == '1':
                self.show_inventory()
                continue
            # If user presses 2, go to sort inventory menu
            elif user_input == '2':
                self.display_sort_inventory_menu()
                continue
            # If user presses 'r', return to main menu
            elif user_input == 'r':
                #Print newline
                print()
                break
            # Otherwise, print invalid input message
            else:
                print("\nInvalid input. Please try again.")

    # Displays the inventory viewing menu
    def show_inventory(self):
        """
            Displays the inventory viewing menu
            Current inventory is displayed
            User can return to main menu by pressing 'r'
        """
        # Prints newline
        print()

        # Puts "Current Inventory" header in borders
        header = "Current Inventory"
        self.draw_header_with_borders(header)

        # Displays inventory
        self.inventory.display_inventory()

        # Prints newline
        print()

        # Draws border to separate inventory from totals
        self.draw_border()

        # Displays totals (unique items and total quantities)
        self.inventory.display_totals()

        # Waits for user to press Enter to return to View Inventory Menu (pause screen)
        input("Press Enter to return to View Inventory Menu...")

    # Shows sort inventory menu
    def display_sort_inventory_menu(self):
        """
            Displays the sort inventory menu
            Shows the following options to sort by:
            (1) Name
            (2) Container
            (3) Food Group
            (4) Weight
            (5) Quantity
        """

        # If inventory is empty, show message and exit function
        if not self.inventory.items:
            print("\nInventory is empty. Nothing to sort.")
            return

        # Map user input to sort field and display name
        sort_options = {
            '1': ('name', 'Name'),
            '2': ('container', 'Container'),
            '3': ('food_group', 'Food Group'),
            '4': ('weight', 'Weight'),
            '5': ('quantity', 'Quantity')
        }

        # Ask what to sort by and validate input
        # Prints newline
        while True:
            print()
            # Puts "SORT INVENTORY" header in borders
            header = "SORT INVENTORY"
            self.draw_header_with_borders(header)

            # Prints newline
            print()

            # Print menu and record user input
            print("Sort by:")

            # Print map
            for key, (_, title) in sort_options.items():
                print(f"({key}) {title}")
            
            # Prints newline
            print()

            # Ask user to choose an option
            user_input = input("Choose one of the following options: ").strip()

            # If user input matches map, sort by what matches to the input
            if user_input in sort_options:
                sort_by, sort_title = sort_options[user_input]
                break
            # If user presses any other key, print invalid input message
            else:
                print("\nInvalid input. Please try again.")

        # Ask for ascending/descending order and validate input
        while True:
            print()
            # Print options
            print("Sort order:")
            print("(1) Ascending (A-Z)/(1-9)")
            print("(2) Descending (Z-A)/(9-1)\n")

            #Store user input
            order_input = input("Enter order choice: ").strip()

            # If user presses 1, choose ascending order
            if order_input == '1':
                reverse = False
                order = "Ascending"
                break
            # If user presses 2, choose descending order
            elif order_input == '2':
                reverse = True
                order = "Descending"
                break
            # Otherwise, print invalid input option
            else:
                print("\nInvalid input. Please try again.")

        # Sort inventory according to input (sort_by and reverse)
        sorted_items = self.inventory.get_sorted_items(sort_by=sort_by, reverse = reverse)

        # Display sorted items
        self.display_sorted_items(sorted_items, sort_title, order)
    
        # Waits for user to press Enter to return to View Inventory Menu (pause screen)
        input("Press Enter to return to View Inventory Menu...")

    # Display sorted items
    def display_sorted_items(self, sorted_items, sort_by, order):
        """Shows the sorted items"""
        #Print newline
        print()
    
        # Print header with sorting information (sort_by and order (ascending or descending))
        header = f"Sorted Items - {sort_by} ({order})"
        self.draw_header_with_borders(header)

        #Print newline
        print()

        # If inventory is empty, print message and exit
        if not sorted_items:
            print("\nInventory is empty. Nothing to sort.")
            return

        # Print each item from inventory
        for item in sorted_items:
            formatted_weight = format_unit(item.weight)
            print(f"{item.name.title()} ({formatted_weight}, {item.container.title()}, {item.food_group.title()}) - Qty: {item.quantity}")

        # Print newline
        print()

        # Draws border to separate inventory from totals
        self.draw_border()

        # Displays totals (unique items and total quantities)
        self.inventory.display_totals()

    # Helper function to decide which item from inventory to add/remove
    def choose_item_from_matches(self, matching_keys):
        """
            Prompts the user to choose one item when multiple matches exist

            Useful for the case where there are items of the same name, container, and weight
            but different food groups

            Returns selected key from matching keys (specific item)
            Returns None if user cancels
        """
        # Prints a numbered list of items from matching keys
        # Ex:
        # 1) Cereal (Box, Grains, 12 oz) - 10 available
        print("\nMultiple matching items found:")
        for i, k in enumerate(matching_keys, start=1):
            item = self.inventory.items[k]
            print(
                f"{i}) {item.name.title()} "
                f"({item.container.title()}, {item.food_group.title()}, {item.weight}) "
                f"- {item.quantity} available"
            )
        # Option to cancel selection
        print("\n0) Cancel")

        # Prompts user for input
        while True:
            user_input = input("\nEnter your choice: ").strip()

            # If user does not enter a digit, print error message and return to the start of the loop
            if not user_input.isdigit():
                print("\nPlease enter a number.\n")
                continue

            # Otherwise, user has entered a digit, so store it as an int
            user_input = int(user_input)

            # If user chooses 0, return None (cancel selection)
            if user_input == 0:
                return None
            # If user chooses one of the options (between 1 and the max number of items),
            # return the corresponding item
            elif 1 <= user_input <= len(matching_keys):
                # user_input - 1: subtracted 1 for indexing
                return matching_keys[user_input - 1]
            # Otherwise, user has chosen an invalid option (outside of range), so print error message and
            # return to the start of the loop
            else:
                print("\nInvalid selection. Please try again.\n")

    # Helper function to display item info
    def display_item_info(self, item, header_message):
        """
            Displays item info (name, container, food_group, weight, and quantity)
        """
        print(f"\n{header_message}")
        print(f"\n{item.name.title()} ({item.container.title()}, {item.food_group.title()}, {item.weight})")
        print(f"Current quantity: {item.quantity}")

    # Displays add items menu that asks for user input
    def add_item_menu(self):
        """Prompts user to input the following information to add item: name, category, weight, and quantity
           Handles multiple items with the same name, container, and weight but different food groups
           Quantity must be an int, so it checks for that
           Confirms removal and quantity before updating inventory
           User must press 'R' to return to menu
        """   
        # Prints newline
        print()
        # Puts "Add Items" in borders
        header = "ADD ITEM"
        self.draw_header_with_borders(header)
        # Prints newline
        print()

        # Keep asking until user confirms to add item to inventory
        while True:
            # Print user prompt messages
            print("Fill out the following information below:\n")

            # Check for valid name input (not empty)
            while True:
                name = input("Item name: ").strip().lower()

                if name:
                    break
                print("\nName cannot be empty.\n")

            # Check for valid container input (not empty)
            while True:
                container = input("Container (Can, Box, Jar, etc.): ").strip().lower()

                if container:
                    break
                print("\nContainer cannot be empty.\n")

            # Check for valid weight input
            while True:
                weight_input = input("Weight (ex. 12 oz, 2 lb): ").strip().lower()

                # If user has not entered anything (empty string), print error message
                # And return to the start of the loop
                if not weight_input:
                    print("\nWeight cannot be empty.\n")
                    continue

                # Valid user input
                # If successful, break from loop and continue to the next step
                try:
                    formatted_weight = format_unit(weight_input)
                    break
                # Otherwise, print error message
                except ValueError as e:
                    print(f"\nInvalid weight: {e}\n")

            # Won't exit until user inputs a valid response (int) for quantity
            while True:
                quantity_input = input("Quantity: ").strip()

                # If input is a string of digits (resulting in int), continue to the next step
                if quantity_input.isdigit() and int(quantity_input) > 0:
                    quantity = int(quantity_input)
                    break
                # Otherwise, print invalid quantity and ask for a number
                else:
                    print("\nInvalid quantity. Please enter a positive whole number greater than 0.\n")

            # Defining food_group to ensure it does not cause an error if checked before defined
            food_group = None
            # Flag to confirm existing item in inventory
            confirmed_existing = False

            # Check if item exists (has the same name, container, and weight (ignoring food_group))
            partial_key = (name.lower(), container.lower(), formatted_weight.lower())
            matching_keys = [k for k in self.inventory.items if (k[0], k[1], k[3]) == partial_key]
            # Header message for adding to an existing item
            header_message = "This item is already in inventory."

            if matching_keys:
                # If item exists and there is only one match, automatically select the item
                if len(matching_keys) == 1:
                    # key stores the first (and only) item in matching keys
                    key = matching_keys[0]
                # If item exists and there are multiple matches (same name, container, weight but different food groups)
                # Ask user which item is being referenced
                else:
                    key = self.choose_item_from_matches(matching_keys)
                    header_message = "You chose this item:"

                    if key is None:
                        print("\nSelection canceled.")
                        if not self.get_confirmation("Do you want to try again?"):
                            print("\nReturning to Main Menu.\n")
                            return
                        else:
                            print()
                            continue

                # Show existing item
                item = self.inventory.items[key]
                food_group = item.food_group
                self.display_item_info(item, header_message)

                # Prompt user for confirmation to add to existing item
                # If user decides to not add, ask if they want to try again
                if not self.get_confirmation(f"Add {quantity} more to this item?"):
                    # If user does not want to try again, return to Main Menu
                    if not self.get_confirmation("Do you want to try again?"):
                        print("\nReturning to Main Menu.\n")
                        return
                    # Otherwise, user wants to try again, so return to the start of the loop,
                    # restarting the process to add an item
                    print()
                    continue

                # User already confirmed adding to existing item
                confirmed_existing = True
            # Otherwise, user is entering a new item, so ask for food group
            else:
                # Check for valid food group input
                valid_groups = CANONICAL_FOOD_GROUPS

                while True:
                    fg_input = input(f"Food Group ({', '.join(valid_groups)}): ").strip().lower()

                    if fg_input in VARIATION_FOOD_GROUP_MAP:
                        food_group = VARIATION_FOOD_GROUP_MAP[fg_input]
                        break
                    print("\nInvalid food group. Please enter a valid option.\n")

            # Safety check to guarantee that food_group exists before use
            assert food_group is not None

            # If this is a new item, prompt user to confirm item to add to inventory
            if not confirmed_existing:
                # Confirm item before adding it to inventory
                print(f"\nYou entered: {quantity} {name.title()} ({container.title()}, {food_group.title()}, {formatted_weight})")
                # If user chooses to not add item, print cancelation message and ask if user wants to try again
                if not self.get_confirmation("Do you want to add this item?"):
                    print("\nAdding item canceled.")
                    # If user says no (do not want to try again), exit function and print "Returning to Main Menu"
                    if not self.get_confirmation("Do you want to try again?"):
                        print("\nReturning to Main Menu.\n")
                        return
                    # If user says yes (wants to try again), loop will repeat
                    # Add newline
                    else:
                        print()
                        continue
            # If user chooses to add item, break from loop (continue to the next step) 
            break

        # If the item is new, create its key (with food group)
        # Existing item already has a partial key (no food group), so it will be given a full key too
        key = self.inventory.make_key(name, container, food_group, formatted_weight)

        # Add item to inventory and print input
        self.inventory.add_item(name, container, food_group, formatted_weight, quantity)

        # Get updated quantity to show new total
        total_quantity = self.inventory.items[key].quantity
    
        # Prints that item has been added to inventory
        print(f"\n{quantity} {name.title()} ({container.title()}, {food_group.title()}, {formatted_weight}) added to inventory.")
        print(f"New total quantity: {total_quantity}\n")

        # Waits for user to press Enter to return to Main Menu (pause screen)
        input("Press Enter to return to Main Menu...")
        # Prints newline for extra space
        print()

    #Displays remove items menu that asks for user input
    def remove_item_menu(self):
        """Prompts user to input the following information to remove item: name, category, size, and quantity
           Handles multiple items with the same name, container, and weight but different food groups
           Quantity must be an int, so it checks for that
           Confirms removal and quantity before updating inventory
           User must press 'R' to return to menu
        """
    
        # If inventory is empty, show message and exit function
        if not self.inventory.items:
            print("\nInventory is empty. Nothing to remove.\n")
            return

        # Prints newline
        print()
        # Puts "Remove Item" in borders
        header = "REMOVE ITEM"
        self.draw_header_with_borders(header)
        # Prints newline
        print()

        # Prompt for item information until user enters a valid item from inventory
        while True:
            # Print user prompt messages
            print("Fill out the following information below:\n")

            # Check for valid name input (not empty)
            while True:
                name = input("Item name: ").strip().lower()

                if name:
                    break
                print("\nName cannot be empty.\n")

            # Check for valid container input (not empty)
            while True:
                container = input("Container (Can, Box, Jar, etc.): ").strip().lower()

                if container:
                    break
                print("\nContainer cannot be empty.\n")

            # Check for valid weight input
            while True:
                weight_input = input("Weight (ex. 12 oz, 2 lb): ").strip().lower()

                # If user has not entered anything (empty string), print error message
                # And return to the start of the loop
                if not weight_input:
                    print("\nWeight cannot be empty.\n")
                    continue

                try:
                    formatted_weight = format_unit(weight_input)
                    break
                except ValueError as e:
                    print(f"\nInvalid weight: {e}\n")

            # Check if item exists (has the same name, container, and weight (ignoring food_group))
            partial_key = (name.lower(), container.lower(), formatted_weight.lower())
            matching_keys = [k for k in self.inventory.items if (k[0], k[1], k[3]) == partial_key]

            # If item is not found in inventory, print error message and ask user to try again
            if not matching_keys:
                print("\nItem not found.")
                prompt = "Do you want to try again?"

                # If user decides to not try again, exit to main menu
                if not self.get_confirmation(prompt):
                    print("\nReturning to Main Menu.\n")
                    return
                # Print newline for repeating steps
                print()
                # Returns to the start of the loop
                continue
            # Otherwise if the item is found in the inventory...
            else:
                header_message = "This item will be removed."
                # If there is only one item of its kind in the inventory (same name, container, weight, and food group)
                if len(matching_keys) == 1:
                    # Pick the first match automatically
                    key = matching_keys[0]
                # Otherwise there are other choices (same name, container, weight but different food groups)
                else:
                    # Set key to chosen item
                    key = self.choose_item_from_matches(matching_keys)
                    header_message = "You chose this item to be removed."

                    # If key is None, user has chosen to cancel selection
                    if key is None:
                        print("\nSelection canceled.")
                        # Ask user if they want to try again
                        # If user does not want to try again, return to Main Menu
                        if not self.get_confirmation("Do you want to try again?"):
                            print("\nReturning to Main Menu.\n")
                            return
                        # Otherwise user wants to try again, so print new line and return to the start of the loop
                        print()
                        continue
            # Store current quantity of item
            available_quantity = self.inventory.items[key].quantity

            # Won't exit until user inputs a valid response (int) for quantity
            while True:
                quantity_input = input("Quantity: ").strip()

                # If input is a string of digits (resulting in int), continue to the next step
                if quantity_input.isdigit():
                    # Storing quantity input as an int
                    quantity = int(quantity_input)

                    # If input is a positive number (> 0) and not greater than the available quantity,
                    # it's a valid response (continue to the next step)
                    if quantity > 0:
                        if quantity <= available_quantity:
                            break
                        else:
                            # If user is asking for more than what's available, print error message and prompt user to try again
                            print(f"\nCannot remove {quantity}. Only {available_quantity} available. Please try again.\n")      
                    # Otherwise, the user entered a number <= 0, so the response is invalid
                    else:
                        print("\nPlease enter a whole number greater than 0.\n")
                # Otherwise, print invalid quantity and ask for a number
                else:
                    print("\nInvalid quantity. Please enter a whole number.\n")

            # Sets food_group to food group of item in key
            food_group = self.inventory.items[key].food_group

            # Confirm item removal
            item = self.inventory.items[key]
            self.display_item_info(item, header_message)
            
            # If user chooses not to remove item, print removal cancelation message and ask if user wants to try again
            prompt = "Do you want to remove this item?"
            if not self.get_confirmation(prompt):
                print("\nRemoval canceled.")
                
                # If user chooses to not try again, return to Main Menu
                prompt = "Do you want to try again?"
                if not self.get_confirmation(prompt):
                    print("\nReturning to Main Menu.\n")
                    return
                # Otherwise, return to the start of the loop for user to try again
                else:
                    print()
                    continue
            # If user chooses to remove item, break from loop (continue to the next step)
            else:
                break

        # Remove item from inventory and print input
        self.inventory.remove_item(name, container, food_group, formatted_weight, quantity)
        print(f"\n{quantity} {name.title()} ({container.title()}, {food_group.title()}, {formatted_weight}) removed from inventory.\n")

        # Waits for user to press Enter to return to Main Menu (pause screen)
        input("Press Enter to return to Main Menu...")

    # Load inventory menu (currently from csv files only)
    def load_inventory_menu(self):
        """
            This function displays the load inventory menu

            It prompts the user for a CSV filename

            If the filename is valid (not empty), it will warn that the current inventory will be
            overwritten and ask user for confirmation

            If user confirms yes to load, program will try to load filename
            If user confirms no, load will be canceled
        """
        # Store current filename
        current_filename = self.inventory.get_current_file()
        # File extention
        file_extension = ".csv"

        # Prints newline
        print()
    
        # Ask for filename
        # Keep asking until user enters a valid name (not empty)
        while True:
            filename_input = input("Enter the CSV filename to load (ex. file_name.csv): ").strip()
            # If user input isn't empty, store it
            if filename_input:
                filename = filename_input
                # If user forgets to add .csv, add it at the end
                if not filename.lower().endswith(file_extension):
                    filename += file_extension
                break
            # Otherwise, print error message
            print("\nFilename cannot be empty. Please try again.\n")

        # If the file doesn't exist in the directory, give error message and return to main menu
        if not os.path.exists(filename):
            print("\nLoad failed.")
            print(f"File '{filename}' not found.") 
            print("Make sure the file is in the same directory as this program.\n")
            return

        # Helper function that loads CSV and saves config
        def proceed_with_load():
            """
                Helper function to load the CSV and save config
            """
            self.inventory.load_inventory_from_csv(filename)
            save_config(self.food_bank_name, filename)
            print(f"Inventory loaded from '{filename}'.\n")

        # If the inventory is not empty, warn that loading will replace current inventory
        # and ask user if they want to save before loading
        if self.inventory.get_changed() and self.inventory.items:
            # Warn user that loading a csv will replace current inventory
            print("\nWARNING: Loading a CSV will replace current inventory.\n")
        
            # Keep running until user gives valid input
            while True:
                print("You have unsaved changes.")
                print("(1) Save")
                print("(2) Save As")
                print("(3) Don't Save and Continue Load")
                print("(R) Cancel Load and Return to Main Menu\n")

                # Ask user to choose an option
                user_input = input("Choose an option: ").strip().lower()

                # If user presses 1, save file under current filename if it exists
                if user_input == '1':
                    # If current filename exists, save under that filename
                    if current_filename:
                        self.inventory.save_inventory_to_csv(current_filename)
                    # Otherwise, follow save as prompt
                    else:
                        self.save_as(file_extension)
                    # If save is successful (changed flag = False), proceed with load
                    if not self.inventory.get_changed():
                        proceed_with_load()
                    # Otherwise, save was unsuccessful (changed flag still equals True), so cancel load
                    else:
                        print("\nNo changes were made. Returning to Main Menu.\n")
                    # Return to main menu (break from loop)
                    break
                # If user presses 2, save as
                elif user_input == '2':
                    self.save_as(file_extension)
                    # If save was successful, proceed with load
                    if not self.inventory.get_changed():
                        proceed_with_load()
                    break
                # If user presses 3, don't save file and proceed with load
                elif user_input == '3':
                    proceed_with_load()
                    break
                # If user presses r, return to Main Menu
                elif user_input == 'r':
                    print("\nLoad canceled. Returning to Main Menu.\n")
                    return
                # If user presses any other key, print invalid input message
                else:
                    print("\nInvalid input. Please try again.\n")
        # Otherwise, not unsaved changes, so proceed with load
        else:
            proceed_with_load()

    # Save inventory menu (currently to csv files only)
    def save_inventory_menu(self):
        """
            This function displays the save inventory menu

            It prompts the user for a CSV filename

            If the filename is valid (not empty), it will check if the filename already exists
            in the directory
        
            If the filename exists, it will warn user that saving will
            overwrite the file and prompt for confirmation

            If user confirms yes to save, program will overwrite the file
            If user confirms no, save will be canceled

            If the filename does not exist, it will save under the filename
        """
        #Print newline
        print()

        # If inventory is empty, show message and exit function
        if not self.inventory.items:
            print("Inventory is empty. Nothing to save.\n")
            return

        filename = self.inventory.get_current_file()
        file_extension = ".csv"

        # Ask what to sort by and validate input
        while True:
            # Puts "SORT INVENTORY" header in borders
            header = "SAVE MENU"
            self.draw_header_with_borders(header)

            # Prints newline
            print()

            # Print menu and record user input
            print("Save Options:")
            print("(1) Save")
            print("(2) Save As")
            print("(R) Return to Main Menu")
        
            # Prints newline
            print()

            # Ask user to choose an option
            user_input = input("Choose an option: ").strip().lower()

            # If user presses 1, save file under current filename if it exists
            if user_input == '1':
                # If current filename exists, save under that filename
                if filename:
                    self.inventory.save_inventory_to_csv(filename)
                    print()
                    break
                # Otherwise, save as and ask for filename
                else:
                    self.save_as(file_extension)
                    print()
                    break
            # If user presses 2, save as and ask for filename
            elif user_input == '2':
                self.save_as(file_extension)
                print()
                break
            # If user presses r, return to Main Menu
            elif user_input == 'r':
                break
            # If user presses any other key, print invalid input message
            else:
                print("\nInvalid input. Please try again.\n")

    # Save as csv file and prompt user to input filename
    def save_as(self, file_extention:str):
        """
            Save as csv file and prompt user to input filename
            If user types filename without .csv extention, program adds it at the end of filename
            Checks if file exists under filename and asks for confirmation to save
        """
        # Prints newline
        print()
    
        # Ask for filename
        # Keep asking until user enters a valid name (not empty)
        while True:
            filename_input = input("Enter the CSV filename to save as (ex. file_name.csv): ").strip()

            # If filename is not empty, save to variable
            if filename_input:
                filename = filename_input
                # If user forgets to add .csv, add it at the end
                if not filename.lower().endswith(file_extention):
                    filename += file_extention
                break
            print("\nFilename cannot be empty. Please try again.\n")

        # If the file already exists, warn that saving will overwrite file
        if os.path.exists(filename):
            prompt = filename + " already exists. Overwrite?"
            confirm = self.get_confirmation(prompt)

            # If user confirms yes, try to save under filename
            if confirm:
                self.inventory.save_inventory_to_csv(filename)
            # Otherwise, cancel save
            else:
                print("\nSave canceled.\n")
        # If the file does not exist, try to save under the filename
        else:
            self.inventory.save_inventory_to_csv(filename)
            # Save data to config
            save_config(self.food_bank_name, filename)

    # Save before quitting menu
    def save_before_quitting_menu(self):
        """
            Function prompts user to choose from 3 options:
            (1) Save and Quit
            (2) Quit Without Saving
            (3) Cancel Quit

            For option 1, program handles the cases whether the save was successful or not
            For options 2 and 3, program prints appropriate message and handles accordingly

            Program also handles invalid responses
        """
        while True:
            # Storing changed flag (True = unsaved changes, False = saved/unchanged)
            inventory_changed = self.inventory.get_changed()
        
            # Print menu and record user input
            print("\nYou have unsaved changes. What would you like to do?\n")
            print("(1) Save and quit")
            print("(2) Quit without saving")
            print("(3) Cancel quit")
            print()
            choice = input("Enter 1, 2, or 3: ").strip()

            # If user presses 1, try to save the current inventory to file
            if choice == '1':
                # Try to save inventory
                self.save_inventory_menu()
                # Storing changed flag (True = unsaved changes, False = saved/unchanged)
                inventory_changed = self.inventory.get_changed()
                # If save is successful, print goodbye message and end program (quit)
                if not inventory_changed:
                    self.print_goodbye()
                    return True
                # Otherwise, the save has failed, so the program will return to menu
                else:
                    print("Returning to Main Menu.\n")
                    return False
            # If user presses 2, end program (quit) without saving
            elif choice == '2':
                prompt = "Are you sure you want to quit without saving?"
                quit_input = self.get_confirmation(prompt)
                if quit_input:
                    print("Quitting without saving. Goodbye!")
                    return True
                else:
                    print("\nQuit canceled. Returning to Main Menu.\n")
                    return False
            # If user presses 3, cancel the quit and return to menu
            elif choice == '3':
                print("\nQuit canceled. Returning to Main Menu.\n")
                return False
            # Otherwise, show invalid input message
            else:
                print("\nInvalid input. Please try again.\n")

    def main_menu(self):
        while not self.end_program:
            # Prints the main menu
            self.print_main_menu()                   
            user_input = input("Choose one of the options above: ").strip().lower()

            #If user presses 1, display inventory
            if user_input == '1':
                self.display_inventory_menu() 
            #If user presses 2, display add item menu
            elif user_input == '2':
                self.add_item_menu()
            # If user presses 3, display remove item menu
            elif user_input == '3':
                self.remove_item_menu()
            # If user presses 4, display load inventory menu
            elif user_input == '4':
                self.load_inventory_menu()
            # If user presses 5, display save inventory menu
            elif user_input == '5':
                self.save_inventory_menu()
            #If user presses 'q' or 'Q', end program
            elif user_input == 'q':
                # Store inventory changed flag (determines if the inventory has been saved before quitting program)
                inventory_changed = self.inventory.get_changed()

                # If a change has been made, display save before quitting menu
                if inventory_changed:
                    self.end_program = self.save_before_quitting_menu()
                # Otherwise, print goodbye message and end program (quit)
                else:
                    print()
                    self.print_goodbye()
                    print()
                    self.end_program = True
            # If user presses any other key, print invalid input message
            else:
                print("\nInvalid input. Please try again.\n")