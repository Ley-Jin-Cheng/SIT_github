

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Abstract base class defining the discount calculation contract."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Applies the discount to an order total and returns the final amount."""
        pass


class NoDiscount(DiscountStrategy):
    """Returns the order total unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Applies a percentage discount (e.g., 10 takes 10% off)."""

    def __init__(self, percentage: float):
        if percentage < 0 or percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100.0)


class BulkDiscount(DiscountStrategy):
    """Subtracts a fixed amount when the total meets or exceeds a threshold."""

    def __init__(self, threshold: float, amount: float):
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and discount amount cannot be negative.")
        self.threshold: float = float(threshold)
        self.amount: float = float(amount)

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return max(0.0, total - self.amount)
        return total


class StudentDiscount(DiscountStrategy):
    """Fourth strategy extending discount options (default 5% off) without editing Order."""

    def __init__(self, percentage: float = 5.0):
        if percentage < 0 or percentage > 100:
            raise ValueError("Student discount percentage must be between 0 and 100.")
        self.percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100.0)