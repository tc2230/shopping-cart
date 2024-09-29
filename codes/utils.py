import re
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from codes.promotion import Discount, Coupon

def round(amount: float, places: int):
    # round half up method
    amount = Decimal(amount)
    try:
        return amount.quantize(Decimal(f"0.{'0'*places}"), rounding=ROUND_HALF_UP)
    except Exception as e:
        raise ValueError('Quantizing error')

def parse_discount(text):
    elements = text.split('|')
    return Discount(elements[0], elements[1], elements[2])

def parse_coupon(text):
    elements = text.split(" ")
    return Coupon(elements[0], elements[1], elements[2])

def parse_product(text):
    elements = re.split(r'\*|\:', text)
    quantity = int(elements[0])
    name = elements[1]
    price = float(elements[2])
    return (quantity, name, price)

def read_input(path):
    # 從檔案讀取輸入
    with open(path, "r") as f:
        text = f.read()
        lines = text.strip().split('\n')

    discounts = []
    cart_items = []
    checkout_date = ""
    coupon = None

    i = 0
    while i < len(lines):
        # 讀取數入
        if lines[i] == "輸入":
            i += 1
            # 讀取促銷折扣
            while lines[i] != '':
                discount = parse_discount(lines[i])
                discounts.append(discount)
                i += 1

        # skip blank
        while lines[i] == '':
            i += 1

        # 讀取商品
        while lines[i] != '':
            item = parse_product(lines[i])
            cart_items.append(item)
            i += 1

        # skip blank
        while lines[i] == '':
            i += 1

        # 讀取結帳日期
        checkout_date = lines[i]
        i += 1

        # 讀取coupon
        if lines[i] != '':
            coupon = parse_coupon(lines[i])
            i += 1

        # skip blank
        while lines[i] == '':
            i += 1

        if lines[i] == "輸出":
            output = lines[i+1]
            break

    return discounts, cart_items, checkout_date, coupon, output
