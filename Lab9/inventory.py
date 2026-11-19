

from product import Product


class Inventory:
    def __init__(self):
        self.products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.product_id) is not None:
            print(f"Error: Product with ID '{product.product_id}' already exists.")
            return False
        self.products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.products.remove(product)
            return product
        return None

    def find_product(self, product_id: str) -> Product | None:
        target = product_id.strip().lower()
        for product in self.products:
            if product.product_id.lower() == target:
                return product
        return None

    def display_all_products(self) -> None:
        if not self.products:
            print("Inventory is currently empty.")
            return
        print("-" * 115)
        print("Current Inventory")
        print("-" * 115)
        for product in self.products:
            product.display_information()
        print("-" * 115)