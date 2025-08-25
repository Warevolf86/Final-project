import os
from Models.customers import Customer
from Models.goods import Goods
from Models.orders import Orders

# Класс для покупателей

class DataBase:
    def __init__(self, filename='customerdata.csv'):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write("ФИО;Email;Номер телефона;Адрес\n")  # заголовок
            print(f"Файл '{self.filename}' создан.")

    def write(self, customer: Customer):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(customer.tocsv() + '\n')
    
    def getall(self) -> list[Customer]:
        customers = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Пропускаем заголовок если он есть
        start = 1 if lines and ';' in lines[0] else 0
        
        for line in lines[start:]:
            try:
                name, mail, tlf, addr = line.strip().split(';')
                c = Customer(name, mail, tlf, addr)
                customers.append(c)
            except ValueError as e:
                print(f"Ошибка обработки строки: {line.strip()}. {e}")
        return customers
    

#Класс для товаров

class GoodsData:
    def __init__(self, filename='goodsdata.csv'):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write("Наименование;Цена\n")  # заголовок
            print(f"Файл '{self.filename}' создан.")
    
    def write(self, good: Goods):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(good.tocsv() + '\n')
    
    def getall(self) -> list[Goods]:
        goods = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # Пропускаем заголовок если он есть
        start = 1 if lines and ';' in lines[0] else 0
        
        for line in lines[start:]:
            try:
                naim, price = line.strip().split(';')
                g = Goods(naim, price)
                goods.append(g)
            except ValueError as e:
                print(f"Ошибка обработки строки: {line.strip()}. {e}")
        return goods
    
# Класс для заказов
class OrdersData:
    def __init__(self, filename='ordersdata.csv'):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write("ID заказа;Клиент;Позиции (наименование,цена,количество,сумма);Общая сумма;Статус\n")
            print(f"Файл '{self.filename}' создан.")
    
    def write(self, order: Orders):
        """Запись заказа в CSV файл"""
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(order.tocsv() + '\n')
    
    def getall(self) -> list[Orders]:
        """Чтение всех заказов из CSV файла"""
        orders = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Пропускаем заголовок если он есть
        start = 1 if lines and ';' in lines[0] else 0
        
        for line in lines[start:]:
            try:
                parts = line.strip().split(';')
                if len(parts) >= 5:
                    order_id, customer_name, items_str, total_price, status = parts[0], parts[1], parts[2], float(parts[3]), parts[4]
                    
                    # Парсим позиции заказа
                    items = []
                    for item_str in items_str.split('|'):
                        item_parts = item_str.split(',')
                        if len(item_parts) == 4:
                            naim, price, quantity, item_total = item_parts
                            items.append((naim, float(price), int(quantity), float(item_total)))
                    
                    order = Orders(int(order_id), customer_name, items, float(total_price), status=status)
                    orders.append(order)
            except ValueError as e:
                print(f"Ошибка обработки строки заказа: {line.strip()}. {e}")
        return orders

