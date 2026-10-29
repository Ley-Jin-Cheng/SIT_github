"""
Main Application: inventory_manager.py
Handles menu execution, user interaction, and JSON file persistence.
"""

import os
import json
from product import Product
from inventory import Inventory

DATA_FILE = "inventory.json"

def load_inventory(filename: str, inventory: Inventory) -> None:
    """Loads product records from JSON and populates the Inventory object."""
    if os.path.exists(filename):
        print(f"{filename} found.")
        try:
            with open(filename, "r", encoding="utf-8") as f:
                records = json.load(f)
                for item in records:
                    inventory.add_product(Product.from_dict(item))
            print("Inventory loaded successfully.")
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error reading {filename}: {e}")
    else:
        print(f"{filename} not found. Starting with an empty inventory.")

def save_inventory(filename: str, inventory: Inventory) -> None:
    """Serializes products from the Inventory object to JSON."""
    print("Saving inventory...")
    try:
        data = [prod.to_dict() for prod in inventory.products]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except IOError as e:
        print(f"Failed to save {filename}: {e}")

def display_menu() -> None:
    print("\nMENU")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")

def handle_add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print(f"A product with ID '{product_id}' already exists.")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid numerical value for price or stock.")
        return

    product = Product(product_id, name, price, stock)
    if inventory.add_product(product):
        print("Product added successfully!")

def handle_update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is not None:
        print("Product Found:")
        print(f"Name: {product.name}")
        print(f"Current Stock: {product.stock}\n")
        try:
            new_stock = int(input("New Stock Quantity: "))
            if product.update_stock(new_stock):
                print("Stock updated successfully!")
        except ValueError:
            print("Invalid stock format. Must be an integer.")
    else:
        print("Product not found.")

def handle_search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is not None:
        print("Product Found")
        print("-" * 50)
        print(f"ID: {product.product_id}")
        print(f"Name: {product.name}")
        print(f"Price: ${product.price:.2f}")
        print(f"Stock: {product.stock}")
        print("-" * 50)
    else:
        print("Product not found.")

def main():
    print("INVENTORY MANAGEMENT SYSTEM")
    inventory = Inventory()
    load_inventory(DATA_FILE, inventory)

    while True:
        display_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            handle_add_product(inventory)
        elif choice == "3":
            handle_update_stock(inventory)
        elif choice == "4":
            handle_search_product(inventory)
        elif choice == "5":
            save_inventory(DATA_FILE, inventory)
        elif choice == "6":
            print("\nSaving inventory before exit...")
            try:
                data = [prod.to_dict() for prod in inventory.products]
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                print("Inventory saved successfully.")
            except IOError as e:
                print(f"Failed to save inventory: {e}")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()