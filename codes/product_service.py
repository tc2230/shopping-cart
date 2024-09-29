class ProductService:
    def __init__(self, data: dict):
        self.category_ref = data

    def check_available(self, name):
        return name in self.category_ref

    def get_category(self, name:str):
        if name in self.category_ref:
            return self.category_ref[name]
        else:
            print(f"目錄中沒有{name}~")
            return None
