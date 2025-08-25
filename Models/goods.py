class Goods:
    def __init__(self, naim, price):
        """
        Конструктор класса Goods.
                
        :param naim: Наименование товара
        :param price: Цена товара

        """
        self.naim = naim
        self.price = price

    @staticmethod
    def validate_price(price):
        return price.isdigit()

    def tocsv(self):
        return f"{self.naim};{self.price}"
        
    def get_good_info(self):
        info = f'Наименование: {self.naim}\nЦена: {self.price}'
        return info
