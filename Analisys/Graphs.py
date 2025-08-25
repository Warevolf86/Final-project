import networkx as nx
import sqlite3
import matplotlib.pyplot as plt

class Graphs:
    def __init__(self):
        pass

    def get_city_goods_data(self):
        """Возвращает данные о товарах по городам"""
        try:
            with sqlite3.connect('BD/my_app.db') as conn: 
                cursor = conn.cursor()
                query = '''
SELECT 
    c.address as city,
    g.naim as product_name,
    SUM(oi.quantity) as total_quantity,
    SUM(oi.item_total) as total_revenue
FROM 
    orders o
INNER JOIN 
    customers c ON o.customer_id = c.id
INNER JOIN 
    order_items oi ON o.id = oi.order_id
INNER JOIN 
    goods g ON oi.good_id = g.id
WHERE 
    c.address IS NOT NULL AND c.address != ''
GROUP BY 
    c.address, g.naim
HAVING 
    SUM(oi.quantity) > 0
ORDER BY 
    c.address, total_quantity DESC
'''
                cursor.execute(query)
                data = cursor.fetchall()
                return data
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return []
    
    def create_city_goods_graph(self):
        """Создает граф связей между городами и товарами"""
        data = self.get_city_goods_data()
        if not data:
            print("Нет данных для построения графа")
            return None
        
        # Создаем граф
        G = nx.Graph()
        
        # Добавляем узлы и ребра
        for city, product, quantity, revenue in data:
            # Добавляем город как узел
            G.add_node(city, type='city', size=quantity/10 + 10)
            
            # Добавляем товар как узел
            G.add_node(product, type='product', size=revenue/100 + 5)
            
            # Добавляем связь между городом и товаром
            G.add_edge(city, product, weight=quantity, revenue=revenue)
        
        return G
    
    def plot_city_goods_graph(self):
        """Строит и отображает граф товаров по городам"""
        G = self.create_city_goods_graph()
        if G is None:
            return
        
        # Создаем график
        plt.figure(figsize=(12, 8))
        
        # Разделяем узлы по типам
        city_nodes = [node for node, attr in G.nodes(data=True) if attr.get('type') == 'city']
        product_nodes = [node for node, attr in G.nodes(data=True) if attr.get('type') == 'product']
        
        # Позиционирование узлов
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Рисуем узлы городов
        nx.draw_networkx_nodes(G, pos, 
                              nodelist=city_nodes,
                              node_color='lightblue',
                              node_size=[G.nodes[node]['size'] * 50 for node in city_nodes],
                              alpha=0.8,
                              label='Города')
        
        # Рисуем узлы товаров
        nx.draw_networkx_nodes(G, pos, 
                              nodelist=product_nodes,
                              node_color='lightgreen',
                              node_size=[G.nodes[node]['size'] * 30 for node in product_nodes],
                              alpha=0.8,
                              label='Товары')
        
        # Рисуем ребра
        edges = G.edges()
        weights = [G[u][v]['weight'] / 10 + 1 for u, v in edges]
        nx.draw_networkx_edges(G, pos, 
                              edgelist=edges,
                              width=weights,
                              alpha=0.5,
                              edge_color='gray')
        
        # Подписи узлов
        nx.draw_networkx_labels(G, pos, 
                               font_size=8,
                               font_weight='bold')
        
        # Легенда
        plt.legend(scatterpoints=1)
        plt.title('Граф товаров по городам\n(Размер узлов показывает популярность товаров)')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def get_city_goods_table(self):
        """Возвращает табличные данные для отображения"""
        data = self.get_city_goods_data()
        if not data:
            return []
        
        # Преобразуем в удобный формат
        table_data = []
        for city, product, quantity, revenue in data:
            table_data.append({
                'Город': city,
                'Товар': product,
                'Количество': quantity,
                'Выручка': f"{revenue:.2f} руб."
            })
        
        return table_data