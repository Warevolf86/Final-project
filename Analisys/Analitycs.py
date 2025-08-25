import pandas as pd
import matplotlib.pyplot as plt
import sqlite3


class Analisys:
    def __init__(self):
        pass

    def get_top_orders(self):
        """Возвращает ТОП 5 заказов по сумме"""
        try:
            with sqlite3.connect('BD/my_app.db') as conn: 
                cursor = conn.cursor()
                top_query = '''
SELECT
    orders.id,
    orders.total_price,
    customers.name
FROM
    orders
INNER JOIN
    customers on orders.customer_id = customers.id
ORDER BY orders.total_price DESC
LIMIT 5
'''
                cursor.execute(top_query)
                top_data = cursor.fetchall()
                return top_data
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return []

    def plot_top_orders(self):
        """Строит график ТОП 5 заказов"""
        data = self.get_top_orders()
        if not data:
            print("Нет данных для построения графика")
            return
        
        # Создаем DataFrame
        df = pd.DataFrame(data, columns=['ID заказа', 'Сумма заказа', 'Клиент'])
        
        # Строим график
        df.plot(x='Клиент', y='Сумма заказа', kind='bar')
        plt.title('ТОП 5 заказов по клиентам')
        plt.xlabel('Клиент')
        plt.ylabel('Сумма заказа')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

