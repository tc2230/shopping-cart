from datetime import date, datetime
from codes.promotion import Discount, Coupon
from codes.utils import round

class CartItem:
    def __init__(self, name: str, quantity: int, price: float, category: str):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.category = category

class Cart:
    def __init__(self):
        self.items = {}
        self.coupon = None
        self.discounts = {}
        self.checkout_date = None

    def set_checkout_date(self, check_date: str):
        self.checkout_date = datetime.strptime(check_date, "%Y.%m.%d").date()

    def add_item(self, name: str, quantity: int, price: float, category: str):
        if name not in self.items:
            self.items[name] = CartItem(name, quantity, price, category)
        else:
            self.items[name].quantity += quantity

    def remove_item(self, name: str, quantity: int):
        if name not in self.items:
            print("購物車中無此商品")
        else:
            self.items[name].quantity -= quantity
            if self.items[name].quantity <= 0:
                self.items.pop(name)

    def empty_items(self):
        self.items = {}

    def empty_discount(self):
        self.discounts = {}

    def empty_coupon(self):
        self.coupon = None

    def empty_cart(self):
        self.empty_items()
        self.empty_discount()
        self.empty_coupon()

    def set_coupon(self, coupon: Coupon):
        self.coupon = coupon

    def add_discount(self, discount: Discount):
        # 目前限定每個類別只能套用一組折扣，以最後帶入的優惠券為準
        self.discounts[discount.category] = discount

    def calculate_amount(self):
        amount = 0
        # 逐商品確認是否需要套用折扣
        for item in self.items.values():
            cat = item.category
            q = item.quantity
            price = item.price

            # validate discount
            discount = self.discounts.get(cat)

            # 若有套用對應類別的折扣且在有效期間，則給予折扣
            if discount and discount.is_valid(self.checkout_date):
                amount += (q * price) * discount.rate
            else:
                amount += q * price

        # 最後套用滿額折價券
        coupon = self.coupon
        if coupon and coupon.is_valid(self.checkout_date):
            if amount >= self.coupon.threshold:
                amount -= self.coupon.discount

        return round(amount, 2)
