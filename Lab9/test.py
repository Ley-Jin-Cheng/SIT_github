

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from supplier import Supplier
from product import PhysicalProduct, DigitalProduct
from product_factory import ProductFactory
from inventory import Inventory
from order import Order, OrderLine
from discount import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount
from inventory_manager import load_products


class TestDiscountStrategies(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP-01", "Test Supplier", "test@supplier.com")
        self.item = ProductFactory.create("physical", "P1", "Desk", 125.0, 10, self.supplier)

    def test_no_discount_default(self):
        order = Order("ORD-1")
        order.add_order_line(self.item, 2)  # Subtotal = 250.0
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_bulk_discount_and_runtime_strategy_swap(self):
        order = Order("ORD-2", BulkDiscount(200, 20))
        order.add_order_line(self.item, 2)  # Subtotal = 250.0
        self.assertAlmostEqual(order.calculate_total(), 230.0)

        # Swap strategy without modifying Order
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_bulk_discount_below_threshold(self):
        order = Order("ORD-3", BulkDiscount(200, 20))
        order.add_order_line(self.item, 1)  # Subtotal = 125.0
        self.assertAlmostEqual(order.calculate_total(), 125.0)

    def test_student_discount_extension(self):
        order = Order("ORD-4", StudentDiscount(5))
        order.add_order_line(self.item, 2)  # Subtotal = 250.0
        self.assertAlmostEqual(order.calculate_total(), 237.5)


class TestProductFactory(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP-01", "Test Supplier", "test@supplier.com")

    def test_create_physical_product(self):
        prod = ProductFactory.create("physical", "P01", "Lamp", 25.0, 5, self.supplier)
        self.assertIsInstance(prod, PhysicalProduct)

    def test_create_digital_product(self):
        prod = ProductFactory.create("digital", "D01", "E-Book", 15.0, 100, self.supplier)
        self.assertIsInstance(prod, DigitalProduct)

    def test_unknown_product_type_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S01", "Installation", 30.0, 5, self.supplier)
        self.assertIn("Unknown product type", str(ctx.exception))


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP-01", "Test Supplier", "test@supplier.com")

    def test_price_must_be_greater_than_zero(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P01", "Free Item", 0.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D01", "Negative Item", -10.0, 5, self.supplier)

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P01", "Lamp", 25.0, -1, self.supplier)

        prod = ProductFactory.create("digital", "D01", "App", 10.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            prod.update_stock(-3)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        prod = ProductFactory.create("physical", "P01", "Lamp", 25.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            OrderLine(prod, 0)
        with self.assertRaises(ValueError):
            OrderLine(prod, -2)


class TestCsvFileLoading(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP-01", "CSV Supplier", "csv@supplier.com")
        self.inventory = Inventory()

    def test_load_products_skips_bad_rows_and_loads_valid_rows(self):
        csv_content = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "digital,D001,Photo Editor,49.90,100\n"
            "service,S001,Installation,30.00,5\n"
            "physical,P002,Office Chair,abc,3\n"
            "physical,P003,Monitor Stand,39.50,7\n"
        )
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", encoding="utf-8") as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                load_products(tmp_path, self.inventory, self.supplier)
            output = buf.getvalue()

            self.assertEqual(len(self.inventory.products), 3)
            self.assertIsNotNone(self.inventory.find_product("P001"))
            self.assertIsNotNone(self.inventory.find_product("D001"))
            self.assertIsNotNone(self.inventory.find_product("P003"))
            self.assertIn("3 products loaded.", output)
            self.assertIn("Load attempt finished.", output)
        finally:
            os.remove(tmp_path)

    def test_missing_file_handled_gracefully(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            load_products("non_existent_products.csv", self.inventory, self.supplier)
        output = buf.getvalue()

        self.assertEqual(len(self.inventory.products), 0)
        self.assertIn("Products file not found", output)
        self.assertIn("Load attempt finished.", output)


if __name__ == "__main__":
    unittest.main()