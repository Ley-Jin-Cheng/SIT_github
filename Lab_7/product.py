"""
Product Module
Defines the CanBeShipped interface, abstract Product base class, 
and concrete PhysicalProduct / DigitalProduct subclasses.
"""

from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style abstract base class specifying shipping capability."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculates and returns the shipping cost for the item."""
        pass


class Product(ABC):
    """Abstract base class representing a generic store product."""

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
        """Updates stock count ensuring no negative numbers."""
        if quantity < 0:
            print("Error: Stock quantity cannot be negative.")
            return False
        self._stock = quantity
        return True

    def display_information(self) -> None:
        """Displays common product information without line break for subclass extension."""
        print(
            f"ID: {self._product_id:<6} | Name: {self.name:<18} | Price: ${self._price:>7.2f} | Stock: {self._stock:>3}",
            end=" | "
        )

    def to_dict(self) -> dict:
        """Serializes common product data into a dictionary."""
        return {
            "product_id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method returning the fulfilment delivery mechanism."""
        pass

    @staticmethod
    def create_from_dict(data: dict):
        """Factory method to construct the appropriate subclass instance from JSON data."""
        ptype = data.get("product_type", "").lower()
        if ptype == "physical":
            return PhysicalProduct(
                product_id=data["product_id"],
                name=data["name"],
                price=float(data["price"]),
                stock=int(data["stock"]),
                weight=float(data.get("weight", 0.0))
            )
        elif ptype == "digital":
            return DigitalProduct(
                product_id=data["product_id"],
                name=data["name"],
                price=float(data["price"]),
                stock=int(data["stock"]),
                download_size=float(data.get("download_size", 0.0))
            )
        else:
            raise ValueError(f"Unknown or missing product type: '{ptype}'")


class PhysicalProduct(Product, CanBeShipped):
    """Represents physical goods requiring courier dispatch and handling."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self._weight = float(weight)

    @property
    def weight(self) -> float:
        return self._weight

    def calculate_shipping_cost(self) -> float:
        """Calculates shipping rate: $5.00 base dispatch + $2.50 per kg."""
        return 5.00 + (self._weight * 2.50)

    def get_fulfilment_info(self) -> str:
        return f"Physical dispatch via courier (Weight: {self._weight:.1f}kg, Shipping: ${self.calculate_shipping_cost():.2f})"

    def display_information(self) -> None:
        """Overrides parent display_information to append physical attributes."""
        super().display_information()
        print(f"Type: Physical | Weight: {self._weight:.1f}kg | Shipping: ${self.calculate_shipping_cost():.2f}")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["product_type"] = "physical"
        data["weight"] = self._weight
        return data


class DigitalProduct(Product):
    """Represents digital goods delivered electronically via download link."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self._download_size = float(download_size)

    @property
    def download_size(self) -> float:
        return self._download_size

    def get_fulfilment_info(self) -> str:
        return f"Delivered digitally via secure download link (Size: {self._download_size:.1f}MB)"

    def display_information(self) -> None:
        """Overrides parent display_information to append digital attributes."""
        super().display_information()
        print(f"Type: Digital  | Size: {self._download_size:.1f}MB")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["product_type"] = "digital"
        data["download_size"] = self._download_size
        return data