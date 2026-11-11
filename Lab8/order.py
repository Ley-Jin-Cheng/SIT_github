

from product import Product


class OrderLine:
    """
    Represents an item entry within an order.
    Lifecycle is strictly owned by Order (Composition).
    Associates with Product without owning it.
    """

    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = int(quantity)

    def calculate_subtotal(self) -> float:
        """Calculates subtotal based on referenced product price and ordered quantity."""
        return self.product.price * self.quantity

    def display_line(self) -> None:
        print(
            f"  - Item: {self.product.name:<18} | Qty: {self.quantity:>3} | "
            f"Unit Price: ${self.product.price:>7.2f} | Subtotal: ${self.calculate_subtotal():>8.2f}"
        )


class Order:
    """
    Represents a customer order.
    Composition: Order creates, manages, and owns its OrderLine items.
    """

    def __init__(self, order_id: str):
        self.order_id: str = str(order_id).strip()
        # Composition: OrderLines are contained within and owned by this Order
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        """
        Creates OrderLine internally and adds it to the order.
        External callers cannot inject pre-existing OrderLine objects.
        """
        if quantity <= 0:
            print("Error: Quantity must be greater than zero.")
            return
        line = OrderLine(product, quantity)
        self.order_lines.append(line)

    def calculate_total(self) -> float:
        """Sums the subtotals of all owned order lines."""
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order(self) -> None:
        print(f"\nOrder Details [ID: {self.order_id}]")
        print("-" * 65)
        if not self.order_lines:
            print("  (Order contains no items)")
        else:
            for line in self.order_lines:
                line.display_line()
        print("-" * 65)
        print(f"Total Order Amount: ${self.calculate_total():.2f}\n")