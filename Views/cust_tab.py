import tkinter as tk
from tkinter import ttk, messagebox
from BD.db import *
from Models.customers import Customer
import sqlite3

class CustomerTab:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.create_customer_tab()
    
    def create_customer_tab(self):
        """Создание вкладки для работы с клиентами"""
        # Создаем фрейм для формы добавления
        form_frame = ttk.LabelFrame(self.parent, text="Добавление нового клиента")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        
        # ФИО
        tk.Label(form_frame, text="ФИО:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.entry_name = tk.Entry(form_frame, width=30)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # E-mail
        tk.Label(form_frame, text="E-mail:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_mail = tk.Entry(form_frame, width=30)
        self.entry_mail.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # Адрес
        tk.Label(form_frame, text="Город:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.entry_addr = tk.Entry(form_frame, width=30)
        self.entry_addr.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        # Телефон
        tk.Label(form_frame, text="Телефон:").grid(row=3, column=0, sticky='e', padx=5, pady=5)       
        self.entry_tlf = tk.Entry(form_frame, width=30)
        self.entry_tlf.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        # Кнопка отправки
        submit_button = tk.Button(form_frame, text="Добавить клиента", command=self.submit, bg='lightgreen')
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Создаем фрейм для списка клиентов
        list_frame = ttk.LabelFrame(self.parent, text="Список клиентов")
        list_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        # Listbox для отображения клиентов
        self.customers_listbox = tk.Listbox(list_frame, height=15, width=90, font=('Courier New', 9))
        self.customers_listbox.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        # Scrollbar для Listbox
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.customers_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.customers_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Кнопка обновления списка
        refresh_btn = tk.Button(list_frame, text="Обновить список", 
                               command=lambda: self.load_customers_to_listbox(),
                               bg='lightblue')
        refresh_btn.grid(row=1, column=0, pady=5)
        
        # Загружаем клиентов при запуске
        self.load_customers_to_listbox()

        # Настройка веса колонок для растягивания
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

    def load_customers_to_listbox(self):
        """Загрузка клиентов из БД в Listbox"""
        self.customers_listbox.delete(0, tk.END)  # Очищаем список
        try:
            with sqlite3.connect('BD/my_app.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, phone, email, address FROM customers ORDER BY name")
                customers = cursor.fetchall()
                
                if not customers:
                    self.customers_listbox.insert(tk.END, "Нет клиентов в базе данных")
                    return
                
                # Добавляем заголовки столбцов
                self.customers_listbox.insert(tk.END, "ID".ljust(5) + " | " + 
                                      "ФИО".ljust(25) + " | " + 
                                      "Телефон".ljust(15) + " | " + 
                                      "Email".ljust(25) + " | " + 
                                      "Город")
                self.customers_listbox.insert(tk.END, "-" * 100)  # Разделительная линия
                
                for customer in customers:
                    customer_id, name, phone, email, address = customer
                    # Форматируем строку с выравниванием
                    self.customers_listbox.insert(tk.END, f"{str(customer_id).ljust(5)} | " +
                                          f"{name.ljust(25)} | " +
                                          f"{phone.ljust(15)} | " +
                                          f"{email.ljust(25)} | " +
                                          f"{address}")
                    
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при загрузке клиентов:\n{str(e)}")
            self.customers_listbox.insert(tk.END, "Ошибка загрузки данных")

    def submit(self):
        """Обработка добавления нового клиента"""
        # Получение данных из полей ввода
        name = self.entry_name.get().strip()
        phone = self.entry_tlf.get().strip()
        address = self.entry_addr.get().strip()
        email = self.entry_mail.get().strip()            

        # Проверка заполненности обязательных полей
        if not name:
            messagebox.showerror("Ошибка", "Поле 'ФИО' обязательно для заполнения")
            self.entry_name.focus_set()
            return
            
        if not phone:
            messagebox.showerror("Ошибка", "Поле 'Телефон' обязательно для заполнения")
            self.entry_tlf.focus_set()
            return
            
        if not email:
            messagebox.showerror("Ошибка", "Поле 'Email' обязательно для заполнения")
            self.entry_mail.focus_set()
            return

        # Валидация данных
        if not Customer.validate_email(email):
            messagebox.showerror("Ошибка", "Неверный формат email\nПример: user@example.com")
            self.entry_mail.select_range(0, tk.END)
            self.entry_mail.focus_set()
            return
            
        if not Customer.validate_phone(phone):
            messagebox.showerror("Ошибка", "Телефон должен содержать только цифры (минимум 10 символов)")
            self.entry_tlf.select_range(0, tk.END)
            self.entry_tlf.focus_set()
            return

        try:
            # Подключение к БД и запись данных
            with sqlite3.connect('BD/my_app.db') as conn:
                cursor = conn.cursor() 
                
                # Проверка на существующего клиента
                cursor.execute("SELECT id FROM customers WHERE email = ? OR phone = ?", (email, phone))
                if cursor.fetchone():
                    messagebox.showerror("Ошибка", "Клиент с таким email или телефоном уже существует")
                    return
                
                # Добавление нового клиента
                cursor.execute(
                    "INSERT INTO customers (name, phone, address, email) VALUES (?,?,?,?)", 
                    (name, phone, address if address else '---', email)
                )
                conn.commit()
            
            # Запись в CSV файл
            customer = Customer(name, email, phone, address)
            db = DataBase()
            db.write(customer)
            
            # Очистка полей после успешного сохранения
            self.entry_name.delete(0, tk.END)
            self.entry_tlf.delete(0, tk.END)
            self.entry_addr.delete(0, tk.END)
            self.entry_mail.delete(0, tk.END)
            
            # Обновляем список клиентов
            self.load_customers_to_listbox()
            
            messagebox.showinfo("Успех", "Данные клиента успешно сохранены")
            self.entry_name.focus_set()  # Фокус на первое поле для нового ввода
                        
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при сохранении в базу данных:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неизвестная ошибка:\n{str(e)}")