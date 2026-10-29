"""
Inventory Module
Responsible for storing and managing a collection of Product objects.
"""

from typing import List, Optional
from product import Product

class Inventory:
    def __init__(self):
        self._products: List[Product] = []

    @property
    def products(self) -> List[Product]:
        return self._products

    def add_product(self, product: Product) -> bool:
        """Adds a Product object to the collection if the ID is unique."""
        if self.search_product(product.product_id) is not None:
            print(f"Error: Product ID '{product.product_id}' already exists.")
            return False
        self._products.append(product)
        return True

    def search_product(self, product_id: str) -> Optional[Product]:
        """Searches for a product by its ID (case-insensitive)."""
        target = product_id.strip().lower()
        for product in self._products:
            if product.product_id.lower() == target:
                return product
        return None

    def display_all(self) -> None:
        """Displays all products in the inventory."""
        if not self._products:
            print("Inventory is currently empty.")
            return
        print("Current Inventory")
        for product in self._products:
            product.display_information()