import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Models.orders import Orders

class TestOrders(unittest.TestCase):
    
    def setUp(self):
        """Настройка тестового заказа"""
        self.items = [
            ("Ноутбук", 50000.0, 1, 50000.0),
            ("Мышь", 1000.0, 2, 2000.0)
        ]
        self.order = Orders(1, "Иван Иванов", self.items, 52000.0, "2023-12-01", "новый")
    
    def test_order_creation(self):
        """Тест создания объекта заказа"""
        self.assertEqual(self.order.order_id, 1)
        self.assertEqual(self.order.customer_name, "Иван Иванов")
        self.assertEqual(self.order.items, self.items)
        self.assertEqual(self.order.total_price, 52000.0)
        self.assertEqual(self.order.order_date, "2023-12-01")
        self.assertEqual(self.order.status, "новый")
    
    def test_tocsv_method(self):
        """Тест преобразования в CSV строку"""
        expected_csv = "1;Иван Иванов;Ноутбук,50000.0,1,50000.0|Мышь,1000.0,2,2000.0;52000.0;новый"
        self.assertEqual(self.order.tocsv(), expected_csv)
    
    def test_get_order_info(self):
        """Тест получения информации о заказе"""
        info = self.order.get_order_info()
        
        # Проверяем наличие ключевой информации
        self.assertIn("Заказ №: 1", info)
        self.assertIn("Клиент: Иван Иванов", info)
        self.assertIn("Статус: новый", info)
        self.assertIn("Общая сумма: 52000.0", info)
        self.assertIn("Ноутбук - 50000.0 руб. x 1 = 50000.0 руб.", info)
        self.assertIn("Мышь - 1000.0 руб. x 2 = 2000.0 руб.", info)
    
    def test_str_method(self):
        """Тест строкового представления"""
        expected_str = "Order#1 (Иван Иванов, 2 позиций, 52000.0 руб.)"
        self.assertEqual(str(self.order), expected_str)
    
    def test_order_without_date_and_status(self):
        """Тест заказа без даты и статуса"""
        order = Orders(2, "Петр Петров", self.items, 52000.0)
        self.assertEqual(order.order_id, 2)
        self.assertEqual(order.customer_name, "Петр Петров")
        self.assertIsNone(order.order_date)
        self.assertEqual(order.status, "новый")

if __name__ == '__main__':
    unittest.main()