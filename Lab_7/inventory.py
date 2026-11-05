"""
Inventory Module
Responsible for aggregating and managing collections of Product instances.
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
        """Adds a Product object to inventory if product_id is unique."""
        if self.search_product(product.product_id) is not None:
            print(f"Error: Product with ID '{product.product_id}' already exists.")
            return False
        self._products.append(product)
        return True

    def search_product(self, product_id: str) -> Optional[Product]:
        """Performs a case-insensitive lookup by product ID."""
        target = product_id.strip().lower()
        for p in self._products:
            if p.product_id.lower() == target:
                return p
        return None

    def display_all(self) -> None:
        """Displays all products using polymorphic display_information calls."""
        if not self._products:
            print("Inventory is currently empty.")
            return
        print("-" * 88)
        print("Current Inventory")
        print("-" * 88)
        for p in self._products:
            p.display_information()
        print("-" * 88)