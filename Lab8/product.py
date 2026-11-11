from abc import ABC, abstractmethod
from supplier import Supplier


class CanBeShipped(ABC):
    """Interface specifying shipping capability."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculates and returns shipping fee."""
        pass


class Product(ABC):
    """
    Abstract base class representing a generic store product.
    Associates with a Supplier (Association: Product knows about Supplier).
    """

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier
    ):
        self._product_id: str = str(product_id).strip()
        self.name: str = str(name).strip()
        self._price: float = float(price)
        self._stock: int = int(stock_quantity)
        # Association: Stores a reference to an independent Supplier object
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

    def update_stock(self, quantity: int) -> bool:
        """Updates stock count ensuring no negative numbers (Preserves LSP)."""
        if quantity < 0:
            print("Error: Stock quantity cannot be negative.")
            return False
        self._stock = quantity
        return True

    def display_information(self) -> None:
        """Displays base product details including supplier information."""
        print(
            f"ID: {self._product_id:<6} | Name: {self.name:<18} | Price: ${self._price:>7.2f} | "
            f"Stock: {self._stock:>3} | Supplier: {self.supplier.name}",
            end=" | "
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method returning the fulfilment delivery mechanism."""
        pass

    def to_dict(self) -> dict:
        """Serializes product data and associated supplier details."""
        return {
            "product_id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
            "supplier": self.supplier.to_dict()
        }

    @staticmethod
    def create_from_dict(data: dict):
        """Reconstructs the appropriate concrete subclass from serialized dictionary data."""
        ptype = data.get("product_type", "").lower()
        supplier_data = data.get("supplier", {})
        supplier = Supplier.from_dict(supplier_data)

        if ptype == "physical":
            return PhysicalProduct(
                product_id=data["product_id"],
                name=data["name"],
                price=float(data["price"]),
                stock_quantity=int(data["stock"]),
                supplier=supplier,
                weight=float(data.get("weight", 0.0))
            )
        elif ptype == "digital":
            return DigitalProduct(
                product_id=data["product_id"],
                name=data["name"],
                price=float(data["price"]),
                stock_quantity=int(data["stock"]),
                supplier=supplier,
                download_size=float(data.get("download_size", 0.0))
            )
        else:
            raise ValueError(f"Unknown or missing product type: '{ptype}'")


class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical good requiring shipping calculation."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float
    ):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self._weight: float = float(weight)

    @property
    def weight(self) -> float:
        return self._weight

    def calculate_shipping_cost(self) -> float:
        """Calculates shipping cost based on weight: $5 base + $2.50 per kg."""
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
    """Represents a virtual product delivered via digital download."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        download_size: float
    ):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self._download_size: float = float(download_size)

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