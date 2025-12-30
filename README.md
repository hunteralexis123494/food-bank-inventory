# Food Bank Inventory System

A command-line Python application designed to help food banks manage inventory by
adding, removing, and organizing food items with consistent categorization and
quantity tracking.

This project focuses on clean program structure, user-friendly CLI workflows,
and handling real-world edge cases such as duplicate items and inconsistent food
group naming.

---

## Features

- Add new food items to inventory
- Update quantities of existing items
- Remove items with confirmation prompts
- Normalize food groups to prevent duplicates
- Organized, menu-driven command-line interface
- Persistent configuration storage

---

## Project Structure

food-bank-inventory/
│
├── main.py                # Application entry point
├── menu_manager.py        # Menu handling and user interaction
├── food_groups.py         # Food group normalization and mapping
├── measurements.py        # Unit formatting and validation
├── config.py              # Sample configuration for demonstration
├── sample_inventory.csv   # Sample inventory data for demonstration
└── README.md

---

## Sample / Demo Data

- **Configuration (`config.py`)**: Contains example settings including the food bank name
  "Sample Community Food Bank". This allows the program to run without requiring a
  real food bank.

- **Inventory CSV (`sample_inventory.csv`)**: Provides sample inventory items to test
  the program and matches the configuration to ensure smooth demonstration.

> These files are included purely for demonstration purposes and to make it easy to
  run the program immediately.

---

## Technologies Used

- Python 3
- Python Standard Library

No external dependencies are required.

---

## How to Run

1. Clone the repository:
   git clone https://github.com/hunteralexis123494/food-bank-inventory.git

2. Navigate to the project directory:
   cd food-bank-inventory

3. Run the application:
   python main.py

---

## Design Decisions

- Modular file structure to improve readability and maintainability
- Explicit user confirmations for destructive actions
- Normalization logic to handle inconsistent user input
- Separation of business logic from user interface logic

---

## Future Improvements

- Unit testing for inventory and normalization logic
- Data export (CSV or JSON)
- Inventory reporting and summaries
- Improved input validation
- Optional GUI or web interface

---

## Author

Alexis Hunter