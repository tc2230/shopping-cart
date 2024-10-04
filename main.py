import json
from codes.utils import *
from codes.cart import Cart, CartItem
from codes.promotion import Discount, Coupon
from codes.product_service import ProductService
from codes.user_service import UserService

if __name__ == "__main__":
    # load data
    with open('./data/products.json', 'r') as f:
        product_data = json.loads(f.read())
    with open('./data/user_discount.json', 'r') as f:
        user_discount_data = json.loads(f.read())

    # create product service, user service and cart
    product_service = ProductService(product_data)
    user_service = UserService(user_discount_data)
    cart = Cart()

    # read input
    path = './test_input/case_c.txt'
    discounts, cart_items, checkout_date, user_id, coupon, output = read_input(path)

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

    # set user
    user_discount_rate = user_service.get_discount_rate(user_id)
    cart.set_user(user_id, user_discount_rate)

    print(cart.calculate_amount())
