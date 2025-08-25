import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Models.goods import Goods

class TestGoods(unittest.TestCase):
    
    def setUp(self):
        """Настройка тестового товара"""
        self.valid_good = Goods("Ноутбук", "50000")
    
    def test_goods_creation(self):
        """Тест создания объекта товара"""
        self.assertEqual(self.valid_good.naim, "Ноутбук")
        self.assertEqual(self.valid_good.price, "50000")

    
    def test_validate_price_invalid(self):
        """Тест валидации некорректной цены"""
        invalid_prices = ["abc", "100,50", "-100", "100$", ""]
        
        for price in invalid_prices:
            with self.subTest(price=price):
                self.assertFalse(Goods.validate_price(price))
    
    def test_get_good_info(self):
        """Тест получения информации о товаре"""
        expected_info = "Наименование: Ноутбук\nЦена: 50000"
        self.assertEqual(self.valid_good.get_good_info(), expected_info)
    
    def test_tocsv_method(self):
        """Тест преобразования в CSV строку"""
        expected_csv = "Ноутбук;50000"
        self.assertEqual(self.valid_good.tocsv(), expected_csv)

if __name__ == '__main__':
    unittest.main()