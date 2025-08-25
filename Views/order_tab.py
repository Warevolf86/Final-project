import tkinter as tk
from tkinter import ttk, messagebox
from BD.db import *
from Models.orders import Orders
import sqlite3

class OrderTab:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.current_order_items = []  # Текущие позиции заказа
        self.create_order_tab()
    
    def load_customers(self):
        """Загрузка клиентов из БД"""
        try:
            with sqlite3.connect('BD/my_app.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM customers ORDER BY name")
                return cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при загрузке клиентов:\n{str(e)}")
            return []
    
    def load_goods(self):
        """Загрузка товаров из БД"""
        try:
            with sqlite3.connect('BD/my_app.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, naim, price FROM goods ORDER BY naim")
                return cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при загрузке товаров:\n{str(e)}")
            return []
    
    def on_customer_select(self, event):
        """Обработчик выбора клиента"""
        selection = self.customer_combobox.current()
        if selection >= 0:
            self.selected_customer = self.customers[selection]
    
    def on_good_select(self, event):
        """Обработчик выбора товара"""
        selection = self.goods_combobox.current()
        if selection >= 0:
            self.selected_good = self.goods[selection]
            good_id, good_name, price = self.selected_good
            self.price_var.set(f"Цена: {price} руб.")
    
    def add_item_to_order(self):
        """Добавление позиции к текущему заказу"""
        if not hasattr(self, 'selected_customer'):
            messagebox.showerror("Ошибка", "Сначала выберите клиента")
            return
            
        if not hasattr(self, 'selected_good'):
            messagebox.showerror("Ошибка", "Выберите товар")
            return
            
        try:
            count = int(self.count_entry.get())
            if count <= 0:
                messagebox.showerror("Ошибка", "Количество должно быть положительным числом")
                return
                
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество")
            return
        
        good_id, good_name, price = self.selected_good
        item_total = price * count
        
        # Добавляем позицию в текущий заказ
        self.current_order_items.append((good_id, good_name, price, count, item_total))
        
        # Обновляем список позиций
        self.update_order_items_list()
        
        # Очищаем поля для следующей позиции
        self.goods_combobox.set('')
        self.count_entry.delete(0, tk.END)
        self.price_var.set("Цена: выберите товар")
        if hasattr(self, 'selected_good'):
            delattr(self, 'selected_good')
        
        messagebox.showinfo("Успех", "Позиция добавлена к заказу")
    
    def update_order_items_list(self):
        """Обновление списка позиций заказа"""
        self.items_listbox.delete(0, tk.END)
        total = 0
        
        for i, (good_id, good_name, price, count, item_total) in enumerate(self.current_order_items, 1):
            self.items_listbox.insert(tk.END, f"{i}. {good_name} - {price} руб. x {count} = {item_total} руб.")
            total += item_total
        
        self.total_var.set(f"Общая сумма: {total} руб.")
    
    def create_order(self):
        """Создание окончательного заказа"""
        if not hasattr(self, 'selected_customer'):
            messagebox.showerror("Ошибка", "Выберите клиента")
            return
            
        if not self.current_order_items:
            messagebox.showerror("Ошибка", "Добавьте хотя бы одну позицию в заказ")
            return
        
        customer_id, customer_name = self.selected_customer
        total = sum(item_total for _, _, _, _, item_total in self.current_order_items)
        
        try:
            with sqlite3.connect('BD/my_app.db') as conn:
                cursor = conn.cursor()
                
                # Создаем заказ
                cursor.execute(
                    "INSERT INTO orders (customer_id, total_price) VALUES (?,?)", 
                    (customer_id, total)
                )
                order_id = cursor.lastrowid
                
                # Добавляем позиции заказа
                for good_id, good_name, price, count, item_total in self.current_order_items:
                    cursor.execute(
                        "INSERT INTO order_items (order_id, good_id, quantity, price, item_total) VALUES (?,?,?,?,?)", 
                        (order_id, good_id, count, price, item_total)
                    )
                
                conn.commit()
            
            # Запись в CSV
            items_for_csv = [(good_name, price, count, item_total) for _, good_name, price, count, item_total in self.current_order_items]
            order = Orders(order_id, customer_name, items_for_csv, total)
            order_db = OrdersData()
            order_db.write(order)
            
            # Очистка формы
            self.clear_form()
            
            messagebox.showinfo("Успех", f"Заказ №{order_id} успешно создан!")
            
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при создании заказа:\n{str(e)}")
    
    def clear_form(self):
        """Очистка формы"""
        self.current_order_items = []
        self.customer_combobox.set('')
        self.goods_combobox.set('')
        self.count_entry.delete(0, tk.END)
        self.items_listbox.delete(0, tk.END)
        self.total_var.set("Общая сумма: 0 руб.")
        self.price_var.set("Цена: выберите товар")
        
        if hasattr(self, 'selected_customer'):
            delattr(self, 'selected_customer')
        if hasattr(self, 'selected_good'):
            delattr(self, 'selected_good')
    
    def load_orders(self):
        """Загрузка заказов из БД в Listbox"""
        self.orders_listbox.delete(0, tk.END)
        try:
            with sqlite3.connect('BD/my_app.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT o.id, c.name, o.total_price, o.order_date, o.status,
                           (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.id) as item_count
                    FROM orders o
                    JOIN customers c ON o.customer_id = c.id
                    ORDER BY o.id DESC
                ''')
                orders = cursor.fetchall()
                
                if not orders:
                    self.orders_listbox.insert(tk.END, "Нет заказов в базе данных")
                    return
                
                # Добавляем заголовки столбцов
                self.orders_listbox.insert(tk.END, "ID".ljust(5) + " | " + 
                                          "Клиент".ljust(20) + " | " + 
                                          "Позиций".ljust(8) + " | " + 
                                          "Сумма".ljust(10) + " | " + 
                                          "Дата")
                self.orders_listbox.insert(tk.END, "-" * 80)
                
                for order in orders:
                    order_id, customer, total_price, order_date,  item_count = order
                    date_str = order_date.split()[0] if order_date else "н/д"
                    self.orders_listbox.insert(tk.END, 
                        f"{str(order_id).ljust(5)} | " +
                        f"{customer.ljust(20)} | " +
                        f"{str(item_count).ljust(8)} | " +
                        f"{str(total_price).ljust(10)} | " +
                        f"{date_str}")
                    
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при загрузке заказов:\n{str(e)}")
            self.orders_listbox.insert(tk.END, "Ошибка загрузки данных")
    
    def show_order_details(self, event):
        """Показать детали заказа"""
        selection = self.orders_listbox.curselection()
        if selection:
            selected_text = self.orders_listbox.get(selection[0])
            order_id = selected_text.split('|')[0].strip()
            
            try:
                with sqlite3.connect('BD/my_app.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT g.naim, oi.price, oi.quantity, oi.item_total
                        FROM order_items oi
                        JOIN goods g ON oi.good_id = g.id
                        WHERE oi.order_id = ?
                    ''', (order_id,))
                    items = cursor.fetchall()
                    
                    details = f"Детали заказа #{order_id}:\n\n"
                    for naim, price, quantity, item_total in items:
                        details += f"{naim} - {price} руб. x {quantity} = {item_total} руб.\n"
                    
                    messagebox.showinfo("Детали заказа", details)
                    
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка БД", f"Ошибка при загрузке деталей заказа:\n{str(e)}")

    def create_order_tab(self):
        # Загружаем данные
        self.customers = self.load_customers()
        self.goods = self.load_goods()
        
        # Создаем фрейм для формы добавления
        form_frame = ttk.LabelFrame(self.parent, text="Создание нового заказа")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        
        # Клиент
        tk.Label(form_frame, text="Клиент:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        customer_names = [f"{customer[0]} - {customer[1]}" for customer in self.customers]
        self.customer_combobox = ttk.Combobox(form_frame, values=customer_names, state="readonly", width=40)
        self.customer_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.customer_combobox.bind('<<ComboboxSelected>>', self.on_customer_select)
        
        # Товар
        tk.Label(form_frame, text="Товар:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        
        goods_names = [f"{good[0]} - {good[1]} ({good[2]} руб.)" for good in self.goods]
        self.goods_combobox = ttk.Combobox(form_frame, values=goods_names, state="readonly", width=40)
        self.goods_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.goods_combobox.bind('<<ComboboxSelected>>', self.on_good_select)
        
        # Количество
        tk.Label(form_frame, text="Количество:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        
        self.count_entry = tk.Entry(form_frame, width=10)
        self.count_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # Цена
        self.price_var = tk.StringVar()
        self.price_var.set("Цена: выберите товар")
        price_label = tk.Label(form_frame, textvariable=self.price_var)
        price_label.grid(row=3, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        
        # Кнопка добавления позиции
        add_item_btn = tk.Button(form_frame, text='Добавить позицию', command=self.add_item_to_order, bg='lightblue')
        add_item_btn.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Список текущих позиций
        items_frame = ttk.LabelFrame(form_frame, text="Текущие позиции заказа")
        items_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        
        self.items_listbox = tk.Listbox(items_frame, height=5, width=70)
        self.items_listbox.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        # Общая сумма
        self.total_var = tk.StringVar()
        self.total_var.set("Общая сумма: 0 руб.")
        total_label = tk.Label(form_frame, textvariable=self.total_var, font=('Arial', 10, 'bold'))
        total_label.grid(row=6, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        
        # Кнопка создания заказа
        create_order_btn = tk.Button(form_frame, text='Создать заказ', command=self.create_order, bg='lightgreen')
        create_order_btn.grid(row=7, column=0, pady=10)
        
        # Кнопка очистки формы
        clear_btn = tk.Button(form_frame, text='Очистить форму', command=self.clear_form, bg='lightcoral')
        clear_btn.grid(row=7, column=2, pady=5)

        # Создаем фрейм для списка заказов
        list_frame = ttk.LabelFrame(self.parent, text="Список заказов")
        list_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        # Listbox для отображения заказов
        self.orders_listbox = tk.Listbox(list_frame, height=15, width=90, font=('Courier New', 9))
        self.orders_listbox.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.orders_listbox.bind('<Double-Button-1>', self.show_order_details)
        
        # Scrollbar для Listbox
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.orders_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.orders_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Кнопка обновления списка
        refresh_btn = tk.Button(list_frame, text="Обновить список", 
                               command=self.load_orders,
                               bg='lightblue')
        refresh_btn.grid(row=1, column=0, pady=5)
        
        # Загружаем заказы при запуске
        self.load_orders()

        # Настройка веса колонок для растягивания
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)