from datetime import date, datetime

class Promotion:
    def __init__(self, valid_date):
        self.valid_date = datetime.strptime(valid_date, "%Y.%m.%d").date() # 只取日期

    def is_valid(self, date_to_check=None):
        if not date_to_check:
            date_to_check = date.today()
        return self.valid_date >= date_to_check

class Coupon(Promotion):
    def __init__(self, valid_date, threshold, discount, category):
        super().__init__(valid_date)
        self.threshold = float(threshold)
        self.discount = float(discount)
        self.category = category

class Discount(Promotion):
    def __init__(self, valid_date, rate, category):
        super().__init__(valid_date)
        self.rate = float(rate)
        self.category = category
