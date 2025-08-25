import tkinter as tk
from tkinter import ttk, messagebox
from BD.db import *
from Models.goods import Goods
import sqlite3

class GoodsTab:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.create_goods_tab()

    def create_goods_tab(self):
        # Создаем фрейм для формы добавления
        form_frame1 = ttk.LabelFrame(self.parent, text="Добавление нового товара")
        form_frame1.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        
        # Поля ввода
        tk.Label(form_frame1, text="Наименование:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.entry_naim = tk.Entry(form_frame1, width=30)
        self.entry_naim.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(form_frame1, text="Цена:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_price = tk.Entry(form_frame1, width=30)
        self.entry_price.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # Кнопка добавления
        add_btn = tk.Button(form_frame1, text='Добавить товар', command=self.add_goods, bg='lightgreen')
        add_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Создаем фрейм для списка товаров
        list_frame1 = ttk.LabelFrame(self.parent, text="Список товаров")
        list_frame1.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Listbox для отображения товаров
        self.goods_listbox = tk.Listbox(list_frame1, height=15, width=90, font=('Courier New', 9))
        self.goods_listbox.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        # Scrollbar для Listbox
        scrollbar = ttk.Scrollbar(list_frame1, orient="vertical", command=self.goods_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.goods_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Кнопка обновления списка
        refresh_btn = tk.Button(list_frame1, text="Обновить список", 
                               command=self.load_goods_to_listbox,
                               bg='lightblue')
        refresh_btn.grid(row=1, column=0, pady=5)
        
        # Загружаем товары при запуске
        self.load_goods_to_listbox()

        # Настройка веса колонок для растягивания
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=1)
        form_frame1.grid_columnconfigure(1, weight=1)
        list_frame1.grid_columnconfigure(0, weight=1)
        list_frame1.grid_rowconfigure(0, weight=1)

    def add_goods(self):
        """Добавление нового товара"""
        # Получание данных о товарах
        naim = self.entry_naim.get().strip()            
        price = self.entry_price.get().strip()

        if not Goods.validate_price(price):
            messagebox.showerror("Ошибка", "Значение поля 'Цена:' должно быть числом")
            self.entry_price.select_range(0, tk.END)
            self.entry_price.focus_set()
            return

        if not naim:
            messagebox.showerror("Ошибка", "Поле 'Наименование' обязательно для заполнения")
            self.entry_naim.focus_set()
            return

        if not price:
            messagebox.showerror("Ошибка", "Поле 'Цена' обязательно для заполнения")
            self.entry_price.focus_set()
            return   

        price = float(price)

        try:
            # Подключение к БД и запись данных
            with sqlite3.connect('BD/my_app.db') as conn:
                cursor = conn.cursor()       
                
                # Добавление нового товара
                cursor.execute(
                    "INSERT INTO goods (naim, price) VALUES (?,?)", 
                    (naim, price)
                )
                conn.commit()
            
            # Запись в CSV файл - ИСПРАВЛЕННАЯ СТРОКА
            good = Goods(naim, price)
            gd = GoodsData()  # Создаем экземпляр GoodsData
            gd.write(good)    # Вызываем write у экземпляра GoodsData
            
            # Очистка полей после успешного сохранения
            self.entry_naim.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            
            # Обновляем список товаров
            self.load_goods_to_listbox()
            
            messagebox.showinfo("Успех", "Данные о товаре успешно сохранены")
            self.entry_naim.focus_set()  # Фокус на первое поле для нового ввода
                        
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при сохранении в базу данных:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неизвестная ошибка:\n{str(e)}")

    def load_goods_to_listbox(self):
        """Загрузка товаров из БД в Listbox"""
        self.goods_listbox.delete(0, tk.END)  # Очищаем список
        try:
            with sqlite3.connect('BD/my_app.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, naim, price FROM goods ORDER BY naim")
                goods = cursor.fetchall()
                
                if not goods:
                    self.goods_listbox.insert(tk.END, "Нет товаров в базе данных")
                    return
                
                # Добавляем заголовки столбцов
                self.goods_listbox.insert(tk.END, "ID".ljust(5) + " | " + 
                                       "Наименование".ljust(25) + " | " + 
                                       "Цена".ljust(10))
                self.goods_listbox.insert(tk.END, "-" * 50)  # Разделительная линия
                
                for item in goods:
                    item_id, naim, price = item
                    # Форматируем строку с выравниванием
                    self.goods_listbox.insert(tk.END, f"{str(item_id).ljust(5)} | " +
                                           f"{naim.ljust(25)} | " +
                                           f"{str(price).ljust(10)}")
                    
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при загрузке товаров:\n{str(e)}")
            self.goods_listbox.insert(tk.END, "Ошибка загрузки данных")