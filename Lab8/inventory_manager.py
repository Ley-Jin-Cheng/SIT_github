

import os
import json
from supplier import Supplier
from product import Product, PhysicalProduct, DigitalProduct
from inventory import Inventory
from order import Order

DATA_FILE = "inventory.json"
DEFAULT_SUPPLIER = Supplier("SUP-01", "Default SIT Tech Supplier", "support@sit-tech.edu.sg")


def load_inventory(filename: str, inventory: Inventory) -> None:
    """Loads products and nested supplier data from JSON into the Inventory."""
    if os.path.exists(filename):
        print(f"Found '{filename}'. Loading inventory...")
        try:
            with open(filename, "r", encoding="utf-8") as f:
                records = json.load(f)
                count = 0
                for item in records:
                    try:
                        prod = Product.create_from_dict(item)
                        inventory.add_product(prod)
                        count += 1
                    except (ValueError, KeyError) as err:
                        print(f"Skipping corrupted record: {err}")
            print(f"Successfully loaded {count} product(s).")
        except (json.JSONDecodeError, IOError) as err:
            print(f"Error loading {filename}: {err}")
    else:
        print(f"'{filename}' not found. Starting with empty inventory.")


def save_inventory(filename: str, inventory: Inventory) -> bool:
    """Saves inventory products and supplier details to JSON."""
    print("Saving inventory...")
    try:
        data = [prod.to_dict() for prod in inventory.products]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Inventory saved successfully to '{filename}'.")
        return True
    except IOError as err:
        print(f"Failed to save {filename}: {err}")
        return False


def display_menu() -> None:
    print("\n" + "=" * 45)
    print("      INVENTORY & ORDER SYSTEM (LAB 8)")
    print("=" * 45)
    print("1. Display All Products (Polymorphic)")
    print("2. Add Product (Physical or Digital)")
    print("3. Update Product Stock")
    print("4. Search Product")
    print("5. Create Customer Order (Composition)")
    print("6. Save Inventory")
    print("7. Exit")
    print("=" * 45)


def handle_add_product(inventory: Inventory) -> None:
    print("\n--- Add New Product ---")
    print("1. Physical Product")
    print("2. Digital Product")
    choice = input("Select product type (1 or 2): ").strip()
    if choice not in ("1", "2"):
        print("Invalid selection.")
        return

    pid = input("Product ID: ").strip()
    if not pid or inventory.find_product(pid) is not None:
        print("Error: Product ID is empty or already exists.")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Unit Price ($): "))
        stock = int(input("Stock Quantity: "))
        if price < 0 or stock < 0:
            print("Price and stock cannot be negative.")
            return
    except ValueError:
        print("Invalid number entered for price or stock.")
        return

    print("\n--- Enter Supplier Details (Association) ---")
    sup_name = input(f"Supplier Name [default: {DEFAULT_SUPPLIER.name}]: ").strip()
    if not sup_name:
        supplier = DEFAULT_SUPPLIER
    else:
        sup_id = input("Supplier ID: ").strip() or "SUP-CUSTOM"
        sup_email = input("Supplier Email: ").strip() or "supplier@example.com"
        supplier = Supplier(sup_id, sup_name, sup_email)

    if choice == "1":
        try:
            weight = float(input("Weight (kg): "))
            product = PhysicalProduct(pid, name, price, stock, supplier, weight)
        except ValueError:
            print("Invalid weight format.")
            return
    else:
        try:
            size = float(input("Download Size (MB): "))
            product = DigitalProduct(pid, name, price, stock, supplier, size)
        except ValueError:
            print("Invalid download size format.")
            return

    if inventory.add_product(product):
        print(f"Product '{name}' added successfully.")


def handle_update_stock(inventory: Inventory) -> None:
    print("\n--- Update Stock ---")
    pid = input("Enter Product ID: ").strip()
    prod = inventory.find_product(pid)
    if prod:
        print(f"Current product: {prod.name} | Current stock: {prod.stock}")
        try:
            qty = int(input("Enter new stock level: "))
            if prod.update_stock(qty):
                print("Stock updated successfully.")
        except ValueError:
            print("Invalid quantity.")
    else:
        print(f"Product '{pid}' not found.")


def handle_search_product(inventory: Inventory) -> None:
    print("\n--- Search Product ---")
    pid = input("Enter Product ID: ").strip()
    prod = inventory.find_product(pid)
    if prod:
        print("\nProduct Match:")
        print("-" * 65)
        prod.display_information()
        print(f"Fulfilment Info: {prod.get_fulfilment_info()}")
        print("-" * 65)
    else:
        print(f"Product '{pid}' not found.")


def handle_create_order(inventory: Inventory) -> None:
    print("\n--- Create Customer Order (Composition Demo) ---")
    order_id = input("Enter Order ID: ").strip()
    if not order_id:
        print("Order ID cannot be empty.")
        return

    # Order creates and manages its own OrderLine objects internally
    order = Order(order_id)

    while True:
        pid = input("Enter Product ID to add to order (or 'done' to complete): ").strip()
        if pid.lower() == "done":
            break
        product = inventory.find_product(pid)
        if not product:
            print(f"Product '{pid}' not found in inventory.")
            continue

        try:
            qty = int(input(f"Enter quantity for '{product.name}': "))
            if qty <= 0:
                print("Quantity must be greater than zero.")
                continue
            order.add_order_line(product, qty)
            print(f"Added {qty} x '{product.name}' to order.")
        except ValueError:
            print("Invalid quantity.")

    order.display_order()


def main():
    inventory = Inventory()
    load_inventory(DATA_FILE, inventory)

    while True:
        display_menu()
        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            inventory.display_all_products()
        elif choice == "2":
            handle_add_product(inventory)
        elif choice == "3":
            handle_update_stock(inventory)
        elif choice == "4":
            handle_search_product(inventory)
        elif choice == "5":
            handle_create_order(inventory)
        elif choice == "6":
            save_inventory(DATA_FILE, inventory)
        elif choice == "7":
            print("\nSaving inventory before exit...")
            save_inventory(DATA_FILE, inventory)
            print("Thank you for using Inventory Management System. Program terminated.")
            break
        else:
            print("Invalid option. Please choose between 1 and 7.")


if __name__ == "__main__":
    main()