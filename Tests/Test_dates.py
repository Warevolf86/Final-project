import unittest
import sys
import os
import sqlite3
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Analisys.Dates import OrDates

class TestDates(unittest.TestCase):
    
    def setUp(self):
        """Настройка тестов"""
        self.dates_analysis = OrDates()
    
    @patch('Analisys.Dates.sqlite3.connect')
    def test_get_orders_dates_success(self, mock_connect):
        """Тест успешного получения заказов по датам"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        test_data = [
            ("2023-12-01", 1500.0),
            ("2023-12-02", 2000.0)
        ]
        mock_cursor.fetchall.return_value = test_data
        
        result = self.dates_analysis.get_orders_dates()
        
        self.assertEqual(result, test_data)
        mock_cursor.execute.assert_called_once()
    
    @patch('Analisys.Dates.sqlite3.connect')
    def test_get_orders_dates_empty(self, mock_connect):
        """Тест получения пустого списка заказов по датам"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        result = self.dates_analysis.get_orders_dates()
        
        self.assertEqual(result, [])
    
    @patch('Analisys.Dates.sqlite3.connect')
    def test_get_orders_dates_error(self, mock_connect):
        """Тест обработки ошибки базы данных"""
        mock_connect.return_value.__enter__.side_effect = sqlite3.Error("DB error")
        
        result = self.dates_analysis.get_orders_dates()
        
        self.assertEqual(result, [])
    
    @patch('Analisys.Dates.OrDates.get_orders_dates')
    @patch('Analisys.Dates.plt.show')
    def test_plot_orders_date_with_data(self, mock_show, mock_get_orders_dates):
        """Тест построения графика с данными"""
        test_data = [
            ("2023-12-01", 1500.0),
            ("2023-12-02", 2000.0)
        ]
        mock_get_orders_dates.return_value = test_data
        
        try:
            self.dates_analysis.plot_orders_date()
            executed_successfully = True
        except:
            executed_successfully = False
        
        self.assertTrue(executed_successfully)
        mock_get_orders_dates.assert_called_once()
    
    @patch('Analisys.Dates.OrDates.get_orders_dates')
    def test_plot_orders_date_no_data(self, mock_get_orders_dates):
        """Тест построения графика без данных"""
        mock_get_orders_dates.return_value = []
        
        try:
            self.dates_analysis.plot_orders_date()
            executed_successfully = True
        except:
            executed_successfully = False
        
        self.assertTrue(executed_successfully)

if __name__ == '__main__':
    unittest.main()