import json
from pathlib import Path

INVENTORY_FILE = Path(__file__).parent / "inventory.txt"


def load_inventory():
    

    try:
        with INVENTORY_FILE.open("r") as file:
            data = json.load(file)

        return data

    except FileNotFoundError:
        print("No inventory file found. Starting with empty inventory.")
        return []

    except json.JSONDecodeError:
        print("Inventory file contains invalid JSON.")
        return []


def save_inventory(order_id, name, amount):
   
    try:
        with INVENTORY_FILE.open("r") as file:
            orders = json.load(file)

    except FileNotFoundError:
        orders = []

    except json.JSONDecodeError:
        orders = []

   
    orders.append({
        "order_id": order_id,
        "name": name,
        "amount": amount
    })
    with INVENTORY_FILE.open("w") as file:
        json.dump(orders, file, indent=4)


def get_valid_name():

    name = input("Enter name of product or quit to exit: ")

    if name.lower() == "quit":
        return "quit"

    if name.strip() == "":
        print("Product name cannot be empty.")
        return None

    return name


def get_valid_input():

    amount = input("Enter Quantity Amount or quit to exit: ")

    if amount.lower() == "quit":
        return "quit"

    try:
        amount = int(amount)

        if amount < 0:
            print("Value cannot be less than 0")
            return None

        return amount

    except ValueError:
        print("Enter a valid number")
        return None


def display_current_orders(transaction_history):
   

    print("\nCurrent Orders:\n")

    if not transaction_history:
        print("No previous orders.")

    else:
        for order in transaction_history:
            print(
                f"{order['order_id']}, "
                f"{order['name']}, "
                f"{order['amount']}"
            )

    print()


def display_new_order(order_id, name, amount):
   

    print("\nNew Order Added:\n")
    print(f"{order_id}, {name}, {amount}")
    print()


def generate_report(total_units, failed_attempts, delivery_count):
    

    print(f"The total delivery made is {delivery_count}")
    print(f"Total units delivered is {total_units}")
    print(f"Total failed/rejected entries: {failed_attempts}")


def main():

    
    transaction_history = load_inventory()

    failed_entries = 0

    
    delivery_count = len(transaction_history)

  
    total_delivery = sum(
        order["amount"] for order in transaction_history
    )

    display_current_orders(transaction_history)

    while True:

       
        name = get_valid_name()

        if name == "quit":
            print("Orders successfully saved to inventory.txt")
            break

        if name is None:
            failed_entries += 1
            continue

       
        amount = get_valid_input()

        if amount == "quit":
            print("Orders successfully saved to inventory.txt")
            break

        if amount is None:
            failed_entries += 1
            continue

        
        delivery_count += 1
        order_id = delivery_count

        
        total_delivery += amount

        
        transaction_history.append({
            "order_id": order_id,
            "name": name,
            "amount": amount
        })

       
        save_inventory(order_id, name, amount)

        
        display_new_order(order_id, name, amount)

    
    print()

    generate_report(
        total_delivery,
        failed_entries,
        delivery_count
    )


if __name__ == "__main__":
    main()