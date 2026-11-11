

from product import Product


class Inventory:
    def __init__(self):
        # Aggregation: Inventory holds a collection of independent Product objects
        self.products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Adds an existing Product object to the inventory if unique."""
        if self.find_product(product.product_id) is not None:
            print(f"Error: Product with ID '{product.product_id}' already exists.")
            return False
        self.products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """
        Removes a matching Product from inventory and returns it.
        The Product is NOT destroyed; it can exist independently or move to another inventory.
        """
        product = self.find_product(product_id)
        if product is not None:
            self.products.remove(product)
            return product
        return None

    def find_product(self, product_id: str) -> Product | None:
        """Locates and returns a product by ID (case-insensitive), or None."""
        target = product_id.strip().lower()
        for p in self.products:
            if p.product_id.lower() == target:
                return p
        return None

    def display_all_products(self) -> None:
        """Displays all products using polymorphic dispatch (LSP compliant)."""
        if not self.products:
            print("Inventory is currently empty.")
            return
        print("-" * 115)
        print("Current Inventory")
        print("-" * 115)
        for product in self.products:
            product.display_information()
        print("-" * 115)