from tkinter import ttk, messagebox
import tkinter as tk
from BD.db import *
import sqlite3
from Views.cust_tab import CustomerTab
from Views.goods_tab import GoodsTab
from Views.order_tab import OrderTab
from Views.analysys_tab import AnalisysTab


def import_customers_from_csv():
    """Импорт клиентов из CSV в базу данных"""
    try:
        db = DataBase()
        customers = db.getall()
        
        if not customers:
            return  # Нет данных для импорта
            
        with sqlite3.connect('BD/my_app.db') as conn:
            cursor = conn.cursor()
            
            for customer in customers:
                # Проверяем, существует ли уже клиент
                cursor.execute("SELECT id FROM customers WHERE email = ? OR phone = ?", 
                             (customer.email, customer.phone))
                if not cursor.fetchone():
                    # Добавляем нового клиента
                    cursor.execute(
                        "INSERT INTO customers (name, phone, address, email) VALUES (?,?,?,?)", 
                        (customer.name, customer.phone, customer.address, customer.email)
                    )
            
            conn.commit()
            
    except Exception as e:
        print(f"Ошибка при импорте клиентов: {e}")

def import_goods_from_csv():
    """Импорт товаров из CSV в базу данных"""
    try:
        good = GoodsData()
        goods = good.getall()
        
        if not goods:
            return  # Нет данных для импорта
            
        with sqlite3.connect('BD/my_app.db') as conn:
            cursor = conn.cursor()
            
            for good in goods:
                # Проверяем, существует ли уже товар
                cursor.execute("SELECT id FROM goods WHERE naim = ? AND price = ?", 
                             (good.naim, good.price))
                if not cursor.fetchone():
                    # Добавляем новый товар
                    cursor.execute(
                        "INSERT INTO goods (naim, price) VALUES (?,?)", 
                        (good.naim, good.price)
                    )
            
            conn.commit()
            
    except Exception as e:
        print(f"Ошибка при импорте товаров: {e}")

def import_orders_from_csv():
    """Импорт заказов из CSV в базу данных"""
    try:
        order_db = OrdersData()
        orders = order_db.getall()
        
        if not orders:
            return  # Нет данных для импорта
            
        with sqlite3.connect('BD/my_app.db') as conn:
            cursor = conn.cursor()
            
            for order in orders:
                # Находим ID клиента по имени
                cursor.execute("SELECT id FROM customers WHERE name = ?", (order.customer_name,))
                customer_result = cursor.fetchone()
                
                if customer_result:
                    customer_id = customer_result[0]
                    
                    # Проверяем, существует ли уже заказ
                    cursor.execute("SELECT id FROM orders WHERE id = ?", (order.order_id,))
                    if not cursor.fetchone():
                        # Создаем заказ
                        cursor.execute(
                            "INSERT INTO orders (id, customer_id, total_price, status) VALUES (?,?,?,?)", 
                            (order.order_id, customer_id, order.total_price, order.status)
                        )
                        
                        # Добавляем позиции заказа
                        for naim, price, quantity, item_total in order.items:
                            # Находим ID товара
                            cursor.execute("SELECT id FROM goods WHERE naim = ? AND price = ?", (naim, price))
                            good_result = cursor.fetchone()
                            
                            if good_result:
                                good_id = good_result[0]
                                cursor.execute(
                                    "INSERT INTO order_items (order_id, good_id, quantity, price, item_total) VALUES (?,?,?,?,?)", 
                                    (order.order_id, good_id, quantity, price, item_total)
                                )
            
            conn.commit()
            
    except Exception as e:
        print(f"Ошибка при импорте заказов: {e}")

# Подключение к БД (файл my_app.db будет создан, если не существует) 
with sqlite3.connect('BD/my_app.db') as conn: 
    cursor = conn.cursor() 
    # Создаем таблицу 
    cursor.execute(''' 
CREATE TABLE IF NOT EXISTS customers ( 
id INTEGER PRIMARY KEY, 
name TEXT NOT NULL,
phone TEXT NOT NULL,
address TEXT NOT NULL,
email TEXT NOT NULL                      
) 
''') 
    cursor.execute('''
CREATE TABLE IF NOT EXISTS goods (
id INTEGER PRIMARY KEY,
naim TEXT NOT NULL,
price REAL NOT NULL)
''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
id INTEGER PRIMARY KEY,
customer_id INTEGER NOT NULL,
total_price REAL NOT NULL DEFAULT 0,
order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
status TEXT DEFAULT 'новый',
FOREIGN KEY (customer_id) REFERENCES customers (id)
)
''')

    cursor.execute('''
CREATE TABLE IF NOT EXISTS order_items (
id INTEGER PRIMARY KEY,
order_id INTEGER NOT NULL,
good_id INTEGER NOT NULL,
quantity INTEGER NOT NULL,
price REAL NOT NULL,
item_total REAL NOT NULL,
FOREIGN KEY (order_id) REFERENCES orders (id),
FOREIGN KEY (good_id) REFERENCES goods (id)
)
''')
    # Импортируем данные из CSV файлов
    import_customers_from_csv()
    import_goods_from_csv()
    import_orders_from_csv()

    # Сохраняем изменения и закрываем соединение 
    conn.commit() 

db = DataBase()
good = GoodsData()    

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение магазина")
        self.root.geometry("850x650")
        
        self.create_notebook()
        self.create_tabs()
        self.add_content_to_tabs()
    
    def create_notebook(self):
        """Создаем виджет Notebook для вкладок"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
    
    def create_tabs(self):
        """Создаем 5 вкладок"""
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)
        self.tab5 = ttk.Frame(self.notebook)
        
        # Добавляем вкладки в Notebook
        self.notebook.add(self.tab1, text="Клиенты")
        self.notebook.add(self.tab2, text="Товары")
        self.notebook.add(self.tab3, text="Заказы")
        self.notebook.add(self.tab4, text="Анализ")
        self.notebook.add(self.tab5, text="Дополнительно")
    




    def add_content_to_tabs(self):
        """Добавляем содержимое на вкладки"""
        # Вкладка 1 - Клиенты
        self.customer_tab = CustomerTab(self.tab1)

        # Вкладка 2 - Товары
        self.goods_tab = GoodsTab(self.tab2)
        
        # Вкладка 3
        self.order_tab = OrderTab(self.tab3)
        
        # Вкладка 4
        self.analisys_tab = AnalisysTab(self.tab4)
        
        # Вкладка 5
        tk.Label(self.tab5, text="О программе", 
                font=('Arial', 10, 'bold')).pack(pady=10)
        tk.Label(self.tab5, 
                text="Версия 1.0\nРазработчик: Рогозин А.Д.\n2025",
                justify='left').pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()