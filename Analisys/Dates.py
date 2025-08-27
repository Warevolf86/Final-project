import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

class OrDates:
    def __init__(self):
        pass

    def get_orders_dates(self):
        """Возвращает сумму заказов по дате"""
        try:
            with sqlite3.connect('BD/my_app.db') as conn: 
                cursor = conn.cursor()
                dates_query = '''
    SELECT
        DATE(orders.order_date) as order_date,
        SUM(orders.total_price) as total_daily_sum
    FROM
        orders
    GROUP BY DATE(orders.order_date)
    ORDER BY order_date
    '''
                cursor.execute(dates_query)
                dates_data = cursor.fetchall()
                
                
                return dates_data
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return []

    def plot_orders_date(self):
        """Строит график заказов по датам"""
        data = self.get_orders_dates()
        if not data:
            print("Нет данных для построения графика")
            return
        
        # Создаем DataFrame
        df = pd.DataFrame(data, columns=['Дата заказа', 'Сумма заказов за день'])
        
        # Строим график
        df.plot(x='Дата заказа', y='Сумма заказов за день', kind='line')
        plt.title('Сумма заказов по датам')
        plt.xlabel('Дата заказа')
        plt.ylabel('Сумма заказов (руб.)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()