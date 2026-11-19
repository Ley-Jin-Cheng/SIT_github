

from abc import ABC, abstractmethod
from supplier import Supplier


class CanBeShipped(ABC):
    """Interface specifying shipping capability."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class Product(ABC):
    """Abstract base class representing a generic store product."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier
    ):
        price_val = float(price)
        stock_val = int(stock_quantity)

        if price_val <= 0:
            raise ValueError("Price must be greater than zero.")
        if stock_val < 0:
            raise ValueError("Stock quantity cannot be negative.")

        self._product_id: str = str(product_id).strip()
        self.name: str = str(name).strip()
        self._price: float = price_val
        self._stock: int = stock_val
        self.supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    def update_stock(self, quantity: int) -> None:
        """Updates stock count, raising ValueError if negative (preserves LSP)."""
        qty = int(quantity)
        if qty < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock = qty

    def display_information(self) -> None:
        print(
            f"ID: {self._product_id:<6} | Name: {self.name:<18} | Price: ${self._price:>7.2f} | "
            f"Stock: {self._stock:>3} | Supplier: {self.supplier.name}",
            end=" | "
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def to_dict(self) -> dict:
        return {
            "product_id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
            "supplier": self.supplier.to_dict()
        }


class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical good requiring shipping."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float = 0.0
    ):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        weight_val = float(weight)
        if weight_val < 0:
            raise ValueError("Weight cannot be negative.")
        self._weight: float = weight_val

    @property
    def weight(self) -> float:
        return self._weight

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (self._weight * 2.50)

    def get_fulfilment_info(self) -> str:
        return f"Physical dispatch via courier (Weight: {self._weight:.1f}kg, Shipping: ${self.calculate_shipping_cost():.2f})"

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Physical | Weight: {self._weight:.1f}kg | Shipping: ${self.calculate_shipping_cost():.2f}")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["product_type"] = "physical"
        data["weight"] = self._weight
        return data


class DigitalProduct(Product):
    """Represents a digital product delivered electronically."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        download_size: float = 0.0
    ):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        size_val = float(download_size)
        if size_val < 0:
            raise ValueError("Download size cannot be negative.")
        self._download_size: float = size_val

    @property
    def download_size(self) -> float:
        return self._download_size

    def get_fulfilment_info(self) -> str:
        return f"Delivered digitally via secure download link (Size: {self._download_size:.1f}MB)"

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Digital  | Size: {self._download_size:.1f}MB")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["product_type"] = "digital"
        data["download_size"] = self._download_size
        return data