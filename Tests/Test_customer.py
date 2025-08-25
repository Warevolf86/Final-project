import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Models.customers import Customer

class TestCustomer(unittest.TestCase):
    
    def setUp(self):
        """Настройка тестового клиента"""
        self.valid_customer = Customer(
            "Иван Иванов", 
            "ivan@example.com", 
            "1234567890", 
            "Москва"
        )
    
    def test_customer_creation(self):
        """Тест создания объекта клиента"""
        self.assertEqual(self.valid_customer.name, "Иван Иванов")
        self.assertEqual(self.valid_customer.email, "ivan@example.com")
        self.assertEqual(self.valid_customer.phone, "1234567890")
        self.assertEqual(self.valid_customer.address, "Москва")
    
    def test_validate_email_valid(self):
        """Тест валидации корректного email"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "user@sub.domain.com"
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(Customer.validate_email(email))
    
    def test_validate_email_invalid(self):
        """Тест валидации некорректного email"""
        invalid_emails = [
            "invalid",
            "invalid@",
            "@example.com",
            "invalid@.com",
            "invalid@com",
            "invalid@example."
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(Customer.validate_email(email))
    
    def test_validate_phone_valid(self):
        """Тест валидации корректного телефона"""
        valid_phones = ["1234567890", "0987654321", "1111111111"]
        
        for phone in valid_phones:
            with self.subTest(phone=phone):
                self.assertTrue(Customer.validate_phone(phone))
    

    
    def test_get_customer_info(self):
        """Тест получения информации о клиенте"""
        expected_info = "Имя: Иван Иванов\nEmail: ivan@example.com\nТелефон: 1234567890\nАдрес: Москва"
        self.assertEqual(self.valid_customer.get_customer_info(), expected_info)
    
    def test_get_customer_info_no_address(self):
        """Тест получения информации о клиенте без адреса"""
        customer = Customer("Иван Иванов", "ivan@example.com", "1234567890", "")
        expected_info = "Имя: Иван Иванов\nEmail: ivan@example.com\nТелефон: 1234567890"
        self.assertEqual(customer.get_customer_info(), expected_info)
    
    def test_tocsv_method(self):
        """Тест преобразования в CSV строку"""
        expected_csv = "Иван Иванов;ivan@example.com;1234567890;Москва"
        self.assertEqual(self.valid_customer.tocsv(), expected_csv)

if __name__ == '__main__':
    unittest.main()