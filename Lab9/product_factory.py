
from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float = 0.0,
        download_size: float = 0.0
    ) -> Product:
        """Creates and returns a Product subclass matching product_type."""
        clean_type = product_type.strip().lower()

        if clean_type == "physical":
            return PhysicalProduct(
                product_id, name, price, stock_quantity, supplier, weight=weight
            )
        elif clean_type == "digital":
            return DigitalProduct(
                product_id, name, price, stock_quantity, supplier, download_size=download_size
            )
        else:
            raise ValueError(f"Unknown product type: {product_type}")