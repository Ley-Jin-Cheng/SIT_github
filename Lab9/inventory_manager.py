
import csv
import json
import os
from supplier import Supplier
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from discount import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount

JSON_FILE = "inventory.json"
CSV_FILE = "products.csv"
DEFAULT_SUPPLIER = Supplier("SUP-01", "Default SIT Tech Supplier", "support@sit-tech.edu.sg")


def get_positive_float(prompt: str) -> float:
    """Prompts until the user enters a valid float greater than zero."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_float(prompt: str) -> float:
    """Prompts until the user enters a valid float of zero or more."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a number that is zero or greater.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 1.5")


def get_non_negative_int(prompt: str) -> int:
    """Prompts until the user enters a valid integer of zero or more."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number that is zero or greater.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 10")


def get_positive_int(prompt: str) -> int:
    """Prompts until the user enters a valid integer greater than zero."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a whole number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 2")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Loads products from a CSV file using ProductFactory and try/except/else/finally."""
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row
            for row_num, row in enumerate(reader, start=2):
                if not row:
                    continue
                try:
                    if len(row) < 5:
                        raise ValueError("Incomplete row data.")
                    product_type = row[0].strip()
                    product_id = row[1].strip()
                    name = row[2].strip()
                    price = float(row[3].strip())
                    stock_quantity = int(row[4].strip())

                    product = ProductFactory.create(
                        product_type, product_id, name, price, stock_quantity, supplier
                    )
                    if inventory.add_product(product):
                        loaded += 1
                except ValueError as err:
                    print(f"Skipping row {row_num} ({row}): {err}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def load_inventory_json(filename: str, inventory: Inventory) -> None:
    """Loads saved JSON inventory through ProductFactory."""
    if not os.path.exists(filename):
        return
    try:
        with open(filename, "r", encoding="utf-8") as f:
            records = json.load(f)
        for item in records:
            try:
                supplier = Supplier.from_dict(item.get("supplier", {}))
                product = ProductFactory.create(
                    product_type=item.get("product_type", ""),
                    product_id=item["product_id"],
                    name=item["name"],
                    price=float(item["price"]),
                    stock_quantity=int(item["stock"]),
                    supplier=supplier,
                    weight=float(item.get("weight", 0.0)),
                    download_size=float(item.get("download_size", 0.0))
                )
                inventory.add_product(product)
            except (ValueError, KeyError) as err:
                print(f"Skipping invalid JSON record: {err}")
    except (json.JSONDecodeError, OSError) as err:
        print(f"Could not load '{filename}': {err}")


def save_inventory_json(filename: str, inventory: Inventory) -> None:
    """Saves inventory records to JSON."""
    try:
        data = [prod.to_dict() for prod in inventory.products]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Inventory saved successfully to '{filename}'.")
    except OSError as err:
        print(f"Failed to save '{filename}': {err}")


def handle_add_product(inventory: Inventory) -> None:
    print("\n--- Add New Product ---")
    product_type = input("Product Type (physical / digital): ").strip().lower()
    product_id = input("Product ID: ").strip()
    if not product_id or inventory.find_product(product_id) is not None:
        print("Error: Product ID cannot be empty or duplicate.")
        return

    name = input("Product Name: ").strip()
    price = get_positive_float("Unit Price ($): ")
    stock = get_non_negative_int("Stock Quantity: ")

    weight = 0.0
    download_size = 0.0
    if product_type == "physical":
        weight = get_non_negative_float("Weight (kg): ")
    elif product_type == "digital":
        download_size = get_non_negative_float("Download Size (MB): ")

    try:
        product = ProductFactory.create(
            product_type=product_type,
            product_id=product_id,
            name=name,
            price=price,
            stock_quantity=stock,
            supplier=DEFAULT_SUPPLIER,
            weight=weight,
            download_size=download_size
        )
        if inventory.add_product(product):
            print(f"Product '{name}' added successfully.")
    except ValueError as err:
        print(f"Could not create product: {err}")


def handle_update_stock(inventory: Inventory) -> None:
    print("\n--- Update Stock ---")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print(f"Product '{product_id}' not found.")
        return

    print(f"Selected: {product.name} | Current Stock: {product.stock}")
    new_qty = get_non_negative_int("Enter new stock quantity: ")
    try:
        product.update_stock(new_qty)
        print("Stock updated successfully.")
    except ValueError as err:
        print(f"Update failed: {err}")


def handle_create_order(inventory: Inventory) -> None:
    print("\n--- Create Customer Order ---")
    order_id = input("Enter Order ID: ").strip()
    if not order_id:
        print("Order ID cannot be empty.")
        return

    print("Select Discount Strategy:")
    print("1. No Discount")
    print("2. Percentage Discount (10% off)")
    print("3. Bulk Discount ($20 off orders >= $200)")
    print("4. Student Discount (5% off)")
    disc_choice = input("Choose strategy (1-4): ").strip()

    strategies = {
        "1": NoDiscount(),
        "2": PercentageDiscount(10),
        "3": BulkDiscount(200, 20),
        "4": StudentDiscount(5),
    }
    strategy = strategies.get(disc_choice, NoDiscount())
    order = Order(order_id, discount=strategy)

    while True:
        pid = input("Enter Product ID to add (or 'done' to finish): ").strip()
        if pid.lower() == "done":
            break
        product = inventory.find_product(pid)
        if product is None:
            print(f"Product '{pid}' not found.")
            continue

        qty = get_positive_int(f"Enter quantity for '{product.name}': ")
        try:
            order.add_order_line(product, qty)
            print(f"Added {qty} x '{product.name}'.")
        except ValueError as err:
            print(f"Could not add item: {err}")

    order.display_order()


def display_menu() -> None:
    print("\n" + "=" * 48)
    print("   INVENTORY & ORDER SYSTEM (LAB 9)")
    print("=" * 48)
    print("1. Display All Products")
    print("2. Add Product (via ProductFactory)")
    print("3. Update Stock")
    print("4. Create Customer Order (with DiscountStrategy)")
    print("5. Load Products from CSV (products.csv)")
    print("6. Save Inventory to JSON")
    print("7. Exit")
    print("=" * 48)


def main() -> None:
    inventory = Inventory()
    load_inventory_json(JSON_FILE, inventory)

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
            handle_create_order(inventory)
        elif choice == "5":
            path = input(f"Enter CSV path [default: {CSV_FILE}]: ").strip() or CSV_FILE
            load_products(path, inventory, DEFAULT_SUPPLIER)
        elif choice == "6":
            save_inventory_json(JSON_FILE, inventory)
        elif choice == "7":
            save_inventory_json(JSON_FILE, inventory)
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose between 1 and 7.")


if __name__ == "__main__":
    main()