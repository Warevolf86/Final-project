🏪 Магазин - Система управления
Полнофункциональное приложение для управления магазином с графическим интерфейсом на Tkinter.

📋 Оглавление
Возможности

Установка

Запуск

Структура проекта

Использование

Тестирование

База данных

Разработчики

🌟 Возможности
📊 Управление данными
Клиенты - добавление, редактирование, просмотр клиентов с валидацией данных

Товары - управление товарами и ценами

Заказы - создание заказов с несколькими позициями

📈 Аналитика и отчеты
ТОП-5 заказов - самые крупные заказы по сумме

Продажи по датам - график динамики продаж

Граф товаров по городам - визуализация популярности товаров в разных городах

💾 Хранение данных
Двойное хранение: SQLite + CSV файлы

Автоматический импорт данных из CSV в базу данных

Резервное копирование данных

🛠️ Установка
Требования
Python 3.8+

Установленные зависимости:

bash
pip install -r requirements.txt
Зависимости
tkinter
sqlite3
pandas
matplotlib
networkx
🚀 Запуск
Основное приложение
Приложение магазина.bat
Запуск тестов
bash
# Тесты моделей
python Test_customer.py
python Test_goods.py
python Test_orders.py

# Тесты аналитики
python Test_analitycs.py
python Test_dates.py
📁 Структура проекта
text
📦 project/
├── 📂 Models/                 # Модели данных
│   ├── customers.py          # Модель клиентов
│   ├── goods.py              # Модель товаров
│   └── orders.py             # Модель заказов
├── 📂 Views/                 # Представления (GUI)
│   ├── cust_tab.py          # Вкладка клиентов
│   ├── goods_tab.py         # Вкладка товаров
│   ├── order_tab.py         # Вкладка заказов
│   └── analysys_tab.py      # Вкладка аналитики
├── 📂 Analisys/             # Модули аналитики
│   ├── Analitycs.py         # ТОП заказы
│   ├── Dates.py             # Анализ по датам
│   └── Graphs.py            # Графы товаров
├── 📂 BD/                   # Работа с данными
│   └── db.py               # Классы для работы с БД и CSV
├── 📂 Tests/                # Тесты
│   ├── Test_customer.py
│   ├── Test_goods.py
│   ├── Test_orders.py
│   ├── Test_analitycs.py
│   └── Test_dates.py
├── main.py                  # Главный файл приложения
└── 📄 requirements.txt      # Зависимости проекта
🖥️ Использование
Вкладка "Клиенты"
Добавление новых клиентов с валидацией email и телефона

Просмотр списка всех клиентов

Автоматическая проверка на дубликаты

Вкладка "Товары"
Управление товарами и ценами

Валидация числовых значений цен

Просмотр всего каталога товаров

Вкладка "Заказы"
Создание заказов с выбором клиента и товаров

Добавление нескольких позиций в заказ

Автоматический расчет общей суммы

Просмотр истории заказов

Вкладка "Анализ"
Визуализация ТОП-5 заказов

График продаж по датам

Интерактивный граф товаров по городам

Табличное представление данных

🧪 Тестирование
Проект включает комплексные unit-тесты для всех компонентов:

Тесты моделей - проверка валидации данных и методов

Тесты аналитики - проверка корректности запросов и построения графиков

Mock-тесты - тестирование с имитацией базы данных

Запуск всех тестов:

bash
python -m unittest discover
🗃️ База данных
Структура БД
sql
-- Клиенты
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Товары
CREATE TABLE goods (
    id INTEGER PRIMARY KEY,
    naim TEXT NOT NULL,
    price REAL NOT NULL
);

-- Заказы
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    total_price REAL NOT NULL DEFAULT 0,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'новый',
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

-- Позиции заказов
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    good_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    item_total REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (good_id) REFERENCES goods (id)
);
Форматы CSV файлов
customerdata.csv: ФИО;Email;Номер телефона;Адрес

goodsdata.csv: Наименование;Цена

ordersdata.csv: ID заказа;Клиент;Позиции;Общая сумма;Статус

👥 Разработчики
Версия: 1.0

Разработчик: Ваше имя

Год: 2023

📄 Лицензия
© 2023 Магазин - Система управления. Все права защищены.

Примечание: Для работы с графиками убедитесь, что установлены все зависимости из requirements.txt. При первом запуске автоматически создадутся необходимые файлы и таблицы базы данных.
