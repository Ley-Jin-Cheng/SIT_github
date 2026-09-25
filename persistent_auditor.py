import json
from pathlib import Path
INVENTORY_FILE = Path(__file__).parent / "inventory.txt"


def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            data = json.load(file)

        return data["total"], data["history"]

    except FileNotFoundError:
        print("No inventory file found. Starting with empty inventory.")
        return 0.0, []

    except json.JSONDecodeError:
        print("Inventory file contains invalid JSON.")
        return 0.0, []

    except KeyError:
        print("Inventory file is missing required data.")
        return 0.0, []


def get_valid_input():

    while True:
        delivery_input = input("Enter delivery amount or quit to exit: ")
        
       
        if delivery_input.lower() == "quit":
            return "quit"
        
      
        try:
            delivery = int(delivery_input)
            if delivery < 0:
                print("Value cannot be less than 0")
                return None  
            return delivery
        except ValueError:
            print("Enter a valid number")
            return None 

def calculate_tax(amount):
   
    return amount * 0.10


def process_delivery(current_total, new_value):

    tax = calculate_tax(new_value)
    updated_total = current_total + new_value + tax
    return round(updated_total, 3)


def generate_report(total_units, failed_attempts, delivery_count):
    """A dedicated function to print the final summary."""
    print(f"Total delivery cost is {round(total_units, 3)}")
    print(f"The total delivery made is {delivery_count}")
    print(f"Total fail/rejected entries {failed_attempts}")



def main():

    
    total_delivery = 0.0
    failed_entries = 0
    delivery_count = 0
    total_delivery, transaction_history = load_inventory()
    delivery_count = len(transaction_history)

    print(total_delivery)
   
    while True:
           result = get_valid_input()
   
           if result == "quit":
               break
           
           if result is None:
               failed_entries += 1
               continue
   
           
           total_delivery = process_delivery(total_delivery, result)
           delivery_count += 1
           
           
           individual_total = round(result * 1.1, 3)
           print(f"Added {individual_total} to total inventory")
   
       
    generate_report(total_delivery, failed_entries, delivery_count)
if __name__ == "__main__":
    main()