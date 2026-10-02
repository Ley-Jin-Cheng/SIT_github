import json
from pathlib import Path

INVENTORY_FILE = Path(__file__).parent / "inventory.json"


def load_inventory():
    """Load inventory from inventory.json."""

    if INVENTORY_FILE.exists():

        print("inventory.json found.")

        try:
            with INVENTORY_FILE.open("r") as file:
                inventory = json.load(file)

            print("Inventory loaded successfully.")
            return inventory

        except json.JSONDecodeError:
            print("Invalid inventory.json.")
            return []

    else:
        print("inventory.json not found.")
        print("Starting with empty inventory.")
        return []


def save_inventory(inventory):
    """Save inventory to inventory.json."""

    with INVENTORY_FILE.open("w") as file:
        json.dump(inventory, file, indent=4)

    print("Inventory saved successfully.")


def display_all(inventory):
    """Display all products."""

    print("\nCurrent Inventory")
    print("-" * 70)

    if not inventory:
        print("No products in inventory.")

    else:
        for product in inventory:
            print(
                f"ID: {product['id']} | "
                f"Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | "
                f"Stock: {product['stock']}"
            )

    print("-" * 70)


def add_product(inventory):
    """Add a new product."""

    print("\nAdd New Product")

    product_id = input("Product ID: ")
    product_name = input("Product Name: ")

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Please enter a valid price and stock quantity.")
        return

    new_product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }

    inventory.append(new_product)

    print("Product added successfully!")


def update_stock(inventory):
    """Update the stock of an existing product."""

    product_id = input("Enter Product ID: ")

    for product in inventory:

        if product["id"] == product_id:

            try:
                new_stock = int(input("Enter new stock quantity: "))
            except ValueError:
                print("Please enter a valid number.")
                return

            product["stock"] = new_stock

            print("Stock updated successfully!")
            return

    print("Product not found.")


def search_product(inventory):
    """Search for a product."""

    search = input("Enter Product ID or Name: ")

    found = False

    for product in inventory:

        if (
            product["id"].lower() == search.lower()
            or product["name"].lower() == search.lower()
        ):

            print("\nProduct Found")
            print("-" * 70)

            print(
                f"ID: {product['id']} | "
                f"Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | "
                f"Stock: {product['stock']}"
            )

            print("-" * 70)

            found = True

    if not found:
        print("Product not found.")


def main():

    inventory = load_inventory()
    
    save_inventory(inventory)

    while True:

        print("""
----------- MENU -----------
1. Display All Products
2. Add Product
3. Update Stock
4. Search Product
5. Save Inventory
6. Exit
----------------------------
""")

        option = input("Enter option: ")

        if option == "1":

            display_all(inventory)
            print("Display Inventory")

        elif option == "2":

            add_product(inventory)
            print("Add Product")

        elif option == "3":

            update_stock(inventory)
            print("update Inventory")

        elif option == "4":

            search_product(inventory)
           

        elif option == "5":

            save_inventory(inventory)
            print("Save Inventory")

        elif option == "6":

            print("Exiting program")
            break

        else:

            print("Invalid option. Please enter 1-6.")


if __name__ == "__main__":
    main()