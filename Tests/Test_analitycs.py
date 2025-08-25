import unittest
import sys
import os
import sqlite3
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Analisys.Analitycs import Analisys

class TestAnalytics(unittest.TestCase):
    
    def setUp(self):
        """Настройка тестов"""
        self.analysis = Analisys()
    
    @patch('Analisys.Analitycs.sqlite3.connect')
    def test_get_top_orders_success(self, mock_connect):
        """Тест успешного получения топ заказов"""
        # Мокируем соединение и курсор
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Мокируем данные
        test_data = [
            (1, 1000.0, "Иван Иванов"),
            (2, 900.0, "Петр Петров"),
            (3, 800.0, "Сидор Сидоров")
        ]
        mock_cursor.fetchall.return_value = test_data
        
        # Вызываем метод
        result = self.analysis.get_top_orders()
        
        # Проверяем
        self.assertEqual(result, test_data)
        mock_cursor.execute.assert_called_once()
    
    @patch('Analisys.Analitycs.sqlite3.connect')
    def test_get_top_orders_empty(self, mock_connect):
        """Тест получения пустого списка заказов"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        result = self.analysis.get_top_orders()
        
        self.assertEqual(result, [])
    
    @patch('Analisys.Analitycs.sqlite3.connect')
    def test_get_top_orders_error(self, mock_connect):
        """Тест обработки ошибки базы данных"""
        mock_connect.return_value.__enter__.side_effect = sqlite3.Error("DB error")
        
        result = self.analysis.get_top_orders()
        
        self.assertEqual(result, [])
    
    @patch('Analisys.Analitycs.Analisys.get_top_orders')
    @patch('Analisys.Analitycs.plt.show')
    def test_plot_top_orders_with_data(self, mock_show, mock_get_top_orders):
        """Тест построения графика с данными"""
        test_data = [
            (1, 1000.0, "Иван Иванов"),
            (2, 900.0, "Петр Петров")
        ]
        mock_get_top_orders.return_value = test_data
        
        # Этот тест в основном проверяет, что метод выполняется без ошибок
        try:
            self.analysis.plot_top_orders()
            executed_successfully = True
        except:
            executed_successfully = False
        
        self.assertTrue(executed_successfully)
        mock_get_top_orders.assert_called_once()
    
    @patch('Analisys.Analitycs.Analisys.get_top_orders')
    def test_plot_top_orders_no_data(self, mock_get_top_orders):
        """Тест построения графика без данных"""
        mock_get_top_orders.return_value = []
        
        # Проверяем, что метод не падает при отсутствии данных
        try:
            self.analysis.plot_top_orders()
            executed_successfully = True
        except:
            executed_successfully = False
        
        self.assertTrue(executed_successfully)

if __name__ == '__main__':
    unittest.main()