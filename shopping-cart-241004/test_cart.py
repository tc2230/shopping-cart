import json
import pytest
from datetime import date, datetime
from decimal import Decimal
from codes.utils import round
from codes.cart import Cart, CartItem
from codes.promotion import Discount, Coupon
from codes.product_service import ProductService

class TestCart:
    def test_add_item(self):
        cart = Cart()
        cart.add_item("ipad", 2, 2000.0, "電子")
        assert cart.items["ipad"].quantity == 2

    def test_remove_item(self):
        cart = Cart()
        cart.add_item("ipad", 5, 2000.0, "電子")
        cart.remove_item("ipad", 3)
        assert cart.items["ipad"].quantity == 2

    def test_remove_item_not_in_cart(self):
        cart = Cart()
        cart.remove_item("ipad", 1)
        assert cart.items.get("ipad") == None

    def test_remove_item_all(self):
        cart = Cart()
        cart.add_item("ipad", 5, 2000.0, "電子")
        cart.remove_item("ipad", 5)
        assert "ipad" not in cart.items

    def test_set_coupon(self):
        cart = Cart()
        coupon = Coupon("2024.01.01", 100, 10)
        cart.set_coupon(coupon)
        assert cart.coupon == coupon

    def test_add_discount(self):
        cart = Cart()
        discount = Discount("2024.01.01", 0.8, "電子")
        cart.add_discount(discount)
        assert cart.discounts["電子"] == discount

    def test_add_discount_to_same_category(self):
        cart = Cart()
        discount1 = Discount("2024.01.01", 0.85, "電子")
        discount2 = Discount("2024.01.01", 0.75, "電子")
        cart.add_discount(discount1)
        cart.add_discount(discount2)
        assert cart.discounts["電子"] == discount2  # 最後套用的折扣為主

    def test_calculate_amount_no_discount(self):
        cart = Cart()
        cart.add_item("ipad", 2, 2399.0, "電子")
        cart.set_checkout_date("2024.01.01")
        assert cart.calculate_amount() == Decimal('4798.00')

    def test_calculate_amount_with_discount(self):
        cart = Cart()
        cart.add_item("apple", 2, 10.0, "fruit")
        cart.set_checkout_date("2024.01.01")
        discount = Discount("2024.01.01", 0.8, "fruit")
        cart.add_discount(discount)
        assert cart.calculate_amount() == 16.00

    def test_calculate_amount_with_coupon(self):
        cart = Cart()
        cart.add_item("ipad", 1, 2000.0, "電子")
        cart.set_checkout_date("2024.01.01")
        coupon = Coupon("2024.01.01", 2000, 200)
        cart.set_coupon(coupon)
        assert cart.calculate_amount() == Decimal('1800.00')

    def test_calculate_amount_with_discount_and_coupon(self):
        cart = Cart()
        cart.add_item("ipad", 1, 2000.0, "電子")
        cart.set_checkout_date("2024.01.01")
        discount = Discount("2024.01.01", 0.8, "電子")
        cart.add_discount(discount)
        coupon = Coupon("2024.01.01", 1000, 100)
        cart.set_coupon(coupon)
        assert cart.calculate_amount() == Decimal('1500.00')

    def test_calculate_amount_with_discount_expired(self):
        cart = Cart()
        cart.add_item("ipad", 1, 2000.0, "電子")
        cart.set_checkout_date("2024.01.01")
        discount = Discount("2023.12.31", 0.8, "電子")
        cart.add_discount(discount)
        assert cart.calculate_amount() == Decimal('2000.00')

    def test_calculate_amount_with_coupon_expired(self):
        cart = Cart()
        cart.add_item("ipad", 1, 2000.0, "電子")
        cart.set_checkout_date("2024.01.01")
        coupon = Coupon("2023.12.31", 2000, 200)
        cart.set_coupon(coupon)
        assert cart.calculate_amount() == Decimal('2000.00')

    def test_calculate_amount_with_different_category_discount(self):
        cart = Cart()
        cart.add_item("ipad", 1, 2000.0, "電子")
        cart.add_item("啤酒", 1, 300.0, "酒類")
        cart.set_checkout_date("2024.01.01")
        discount_3c = Discount("2024.01.01", 0.8, "電子")
        discount_drink = Discount("2024.01.01", 0.5, "酒類")
        cart.add_discount(discount_3c)
        cart.add_discount(discount_drink)
        assert cart.calculate_amount() == Decimal('1750.00')

    def test_calculate_amount_with_different_category_discount_and_coupon(self):
        cart = Cart()
        cart.add_item("ipad", 1, 2000.0, "電子")
        cart.add_item("啤酒", 1, 300.0, "酒類")
        cart.set_checkout_date("2024.01.01")
        discount_3c = Discount("2024.01.01", 0.8, "電子")
        discount_drink = Discount("2024.01.01", 0.5, "酒類")
        cart.add_discount(discount_3c)
        cart.add_discount(discount_drink)
        coupon = Coupon("2024.01.01", 1000, 100)
        cart.set_coupon(coupon)
        assert cart.calculate_amount() == Decimal('1650.00')

    def test_calculate_amount_with_coupon_not_meet_threshold(self):
        cart = Cart()
        cart.add_item("ipad", 1, 2000.0, "電子")
        cart.set_checkout_date("2024.01.01")
        coupon = Coupon("2024.01.01", 3000, 300)
        cart.set_coupon(coupon)
        assert cart.calculate_amount() == Decimal('2000.00')
