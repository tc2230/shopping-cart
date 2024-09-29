import json
import pytest
from codes.utils import *
from codes.cart import Cart, CartItem
from codes.promotion import Discount, Coupon
from codes.product_service import ProductService

@pytest.mark.parametrize("path, expected_amount", [
    ("./test_input/case_a.txt", Decimal('3083.60')),
    ("./test_input/case_b.txt", Decimal('43.54')),
])

def test_calculate_amount(path, expected_amount):
    # load data
    with open('./products/products.json', 'r') as f:
        data = json.loads(f.read())

    # init cart and service
    product_service = ProductService(data)
    cart = Cart()

    # read input
    discounts, cart_items, checkout_date, coupon, output = read_input(path)

    # load input to cart instance
    # add discount
    for discount in discounts:
        cart.add_discount(discount)

    # add items
    for quantity, name, price in cart_items:
        category = product_service.get_category(name)
        if category: # 若輸入商品存在目錄中，才可加入購物車
            cart.add_item(name, quantity, price, category)

    # set checkout_date
    cart.set_checkout_date(checkout_date)

    # set coupon
    cart.set_coupon(coupon)

    assert round(cart.calculate_amount(), 2) == Decimal(output)
