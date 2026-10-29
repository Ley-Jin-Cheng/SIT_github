"""
Product Module
Represents and manages an individual product entity.
"""

class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self._product_id = str(product_id).strip()
        self.name = str(name).strip()
        self._price = float(price)
        self._stock = int(stock)

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    def update_stock(self, quantity: int) -> bool:
        """Updates product stock while enforcing non-negative quantity rules."""
        if quantity < 0:
            print("Error: Stock quantity cannot be negative.")
            return False
        self._stock = quantity
        return True

    def display_information(self) -> None:
        """Displays formatted single-line product details."""
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}")

    def to_dict(self) -> dict:
        """Converts product attributes into a serializable dictionary."""
        return {
            "product_id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Product instance from a dictionary record."""
        return cls(
            product_id=data.get("product_id", ""),
            name=data.get("name", ""),
            price=float(data.get("price", 0.0)),
            stock=int(data.get("stock", 0))
        )