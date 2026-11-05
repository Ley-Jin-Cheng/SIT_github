"""
Main Application: inventory_manager.py
Provides the CLI interface and manages JSON file persistence for Lab 7.
"""

import os
import json
from product import Product, PhysicalProduct, DigitalProduct
from inventory import Inventory

DATA_FILE = "inventory.json"


def load_inventory(filename: str, inventory: Inventory) -> None:
    """Loads product records from JSON, reconstructing the correct concrete subclasses."""
    if os.path.exists(filename):
        print(f"{filename} found.")
        try:
            with open(filename, "r", encoding="utf-8") as f:
                records = json.load(f)
                loaded_count = 0
                for item in records:
                    try:
                        product = Product.create_from_dict(item)
                        inventory.add_product(product)
                        loaded_count += 1
                    except (ValueError, KeyError) as err:
                        print(f"Skipping invalid record: {err}")
            print(f"Inventory loaded successfully ({loaded_count} product(s)).")
        except (json.JSONDecodeError, IOError) as err:
            print(f"Error reading {filename}: {err}")
    else:
        print(f"{filename} not found. Starting with an empty inventory.")


def save_inventory(filename: str, inventory: Inventory) -> bool:
    """Serializes products along with their type identifiers into JSON."""
    print("Saving inventory...")
    try:
        data = [prod.to_dict() for prod in inventory.products]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Inventory saved successfully to {filename}.")
        return True
    except IOError as err:
        print(f"Failed to save {filename}: {err}")
        return False


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
    print("1. Physical Product")
    print("2. Digital Product")
    type_choice = input("Select Product Type (1 or 2): ").strip()

    if type_choice not in ("1", "2"):
        print("Invalid product type selected.")
        return

    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print(f"Product ID '{product_id}' already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if price < 0 or stock < 0:
            print("Price and stock cannot be negative.")
            return
    except ValueError:
        print("Invalid numerical value for price or stock.")
        return

    if type_choice == "1":
        try:
            weight = float(input("Weight (kg): "))
            if weight < 0:
                print("Weight cannot be negative.")
                return
            new_prod = PhysicalProduct(product_id, name, price, stock, weight)
        except ValueError:
            print("Invalid weight format.")
            return
    else:
        try:
            download_size = float(input("Download Size (MB): "))
            if download_size < 0:
                print("Download size cannot be negative.")
                return
            new_prod = DigitalProduct(product_id, name, price, stock, download_size)
        except ValueError:
            print("Invalid download size format.")
            return

    if inventory.add_product(new_prod):
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
        print("\nProduct Found")
        print("-" * 55)
        print(f"ID:           {product.product_id}")
        print(f"Name:         {product.name}")
        print(f"Price:        ${product.price:.2f}")
        print(f"Stock:        {product.stock}")

        if isinstance(product, PhysicalProduct):
            print(f"Type:         Physical Product")
            print(f"Weight:       {product.weight:.1f} kg")
            print(f"Shipping:     ${product.calculate_shipping_cost():.2f}")
        elif isinstance(product, DigitalProduct):
            print(f"Type:         Digital Product")
            print(f"Size:         {product.download_size:.1f} MB")

        print(f"Fulfilment:   {product.get_fulfilment_info()}")
        print("-" * 55)
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
            save_inventory(DATA_FILE, inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()