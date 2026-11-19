

from product import Product
from discount import DiscountStrategy, NoDiscount


class OrderLine:
    """Represents a product and ordered quantity inside an Order."""

    def __init__(self, product: Product, quantity: int):
        qty = int(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product: Product = product
        self.quantity: int = qty

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_line(self) -> None:
        print(
            f"  - Item: {self.product.name:<18} | Qty: {self.quantity:>3} | "
            f"Unit Price: ${self.product.price:>7.2f} | Subtotal: ${self.calculate_subtotal():>8.2f}"
        )


class Order:
    """Represents a customer order using an interchangeable DiscountStrategy."""

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.order_id: str = str(order_id).strip()
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Replaces the active discount strategy on this order."""
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Creates an OrderLine internally (Composition)."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        """Calculates the subtotal and applies the active discount strategy."""
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_order(self) -> None:
        raw_total = sum(line.calculate_subtotal() for line in self.order_lines)
        final_total = self.calculate_total()
        print(f"\nOrder Details [ID: {self.order_id}]")
        print("-" * 65)
        if not self.order_lines:
            print("  (Order contains no items)")
        else:
            for line in self.order_lines:
                line.display_line()
        print("-" * 65)
        print(f"Subtotal:           ${raw_total:.2f}")
        print(f"Discount Strategy:  {type(self.discount).__name__}")
        print(f"Final Order Total:  ${final_total:.2f}\n")