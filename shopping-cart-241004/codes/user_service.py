class UserService:
    def __init__(self, data: dict):
        self.user_ref = data

    def get_discount_rate(self, user_id: str):
        level = user_id[0]
        if level in self.user_ref:
            return self.user_ref[level]
        else:
            print(f"資料中沒有{level}的會員等級~")
            return None
