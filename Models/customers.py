import re

customer1 = None
class Customer:
    def __init__(self, name, email, phone, address):
        """
        Конструктор класса Customer.
        
        :param name: Имя покупателя
        :param email: Электронная почта
        :param phone: Номер телефона
        :param address: Адрес
        """
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

         

    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        return phone.isdigit() and len(phone) >= 10


    def get_customer_info(self):
        """Возвращает информацию о покупателе."""
        info = f"Имя: {self.name}\nEmail: {self.email}\nТелефон: {self.phone}"
        if self.address:
            info += f"\nАдрес: {self.address}"

        return info 

    def tocsv(self):
        return f"{self.name};{self.email};{self.phone};{self.address}"           

