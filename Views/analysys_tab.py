import networkx as nx
import tkinter as tk
import pandas as pd
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Analisys.Analitycs import Analisys
from Analisys.Dates import OrDates
from Analisys.Graphs import Graphs  # Импортируем новый класс

class AnalisysTab:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.analysis = Analisys()
        self.dates_analysis = OrDates()
        self.graphs_analysis = Graphs()  # Добавляем экземпляр для работы с графами
        self.create_analisys_tab()

    def plot_city_goods_graph(self):
        """Строит граф товаров по городам и отображает в analisys_frame2"""
        # Очищаем предыдущий график
        for widget in self.analisys_frame2.winfo_children():
            widget.destroy()
        
        try:
            # Создаем фигуру matplotlib
            fig = Figure(figsize=(10, 8), dpi=100)
            
            # Строим граф
            G = self.graphs_analysis.create_city_goods_graph()
            if G is None:
                tk.Label(self.analisys_frame2, text="Нет данных для построения графа", 
                        font=('Arial', 12), fg='red').pack(pady=50)
                return
            
            # Разделяем узлы по типам
            city_nodes = [node for node, attr in G.nodes(data=True) if attr.get('type') == 'city']
            product_nodes = [node for node, attr in G.nodes(data=True) if attr.get('type') == 'product']
            
            # Позиционирование узлов
            pos = nx.spring_layout(G, k=1, iterations=50)
            
            # Рисуем граф
            ax = fig.add_subplot(111)
            
            # Рисуем узлы городов
            nx.draw_networkx_nodes(G, pos, 
                                  nodelist=city_nodes,
                                  node_color='lightblue',
                                  node_size=[G.nodes[node]['size'] * 30 for node in city_nodes],
                                  alpha=0.8,
                                  ax=ax,
                                  label='Города')
            
            # Рисуем узлы товаров
            nx.draw_networkx_nodes(G, pos, 
                                  nodelist=product_nodes,
                                  node_color='lightgreen',
                                  node_size=[G.nodes[node]['size'] * 20 for node in product_nodes],
                                  alpha=0.8,
                                  ax=ax,
                                  label='Товары')
            
            # Рисуем ребра
            edges = G.edges()
            weights = [G[u][v]['weight'] / 10 + 1 for u, v in edges]
            nx.draw_networkx_edges(G, pos, 
                                  edgelist=edges,
                                  width=weights,
                                  alpha=0.5,
                                  edge_color='gray',
                                  ax=ax)
            
            # Подписи узлов
            nx.draw_networkx_labels(G, pos, 
                                   font_size=8,
                                   font_weight='bold',
                                   ax=ax)
            
            ax.set_title('Граф товаров по городам\n(Размер узлов показывает популярность/доходность)', 
                        fontsize=12, fontweight='bold')
            ax.legend(scatterpoints=1)
            ax.axis('off')
            
            fig.tight_layout()
            
            # Встраиваем график в Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.analisys_frame2)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Добавляем кнопку для обновления
            refresh_btn = tk.Button(self.analisys_frame2, text="Обновить граф", 
                                   command=self.plot_city_goods_graph, bg='lightblue')
            refresh_btn.pack(pady=5)
            
            # Добавляем кнопку для показа табличных данных
            table_btn = tk.Button(self.analisys_frame2, text="Показать таблицу", 
                                 command=self.show_city_goods_table, bg='lightyellow')
            table_btn.pack(pady=5)
            
        except Exception as e:
            tk.Label(self.analisys_frame2, text=f"Ошибка при построении графа: {str(e)}", 
                    font=('Arial', 12), fg='red').pack(pady=50)

    def show_city_goods_table(self):
        """Показывает табличные данные по товарам в городах"""
        # Очищаем предыдущий график
        for widget in self.analisys_frame2.winfo_children():
            widget.destroy()
        
        data = self.graphs_analysis.get_city_goods_table()
        if not data:
            tk.Label(self.analisys_frame2, text="Нет данных для отображения", 
                    font=('Arial', 12), fg='red').pack(pady=50)
            return
        
        # Создаем таблицу
        tree_frame = ttk.Frame(self.analisys_frame2)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Создаем Treeview
        columns = ('Город', 'Товар', 'Количество', 'Выручка')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Настраиваем заголовки
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Добавляем данные
        for item in data:
            tree.insert('', tk.END, values=(
                item['Город'], 
                item['Товар'], 
                item['Количество'], 
                item['Выручка']
            ))
        
        # Добавляем scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Кнопка возврата к графу
        back_btn = tk.Button(self.analisys_frame2, text="Вернуться к графу", 
                            command=self.plot_city_goods_graph, bg='lightblue')
        back_btn.pack(pady=5)

    def plot_top_orders(self):
        """Строит график ТОП 5 заказов и отображает в analisys_frame2"""
        # Очищаем предыдущий график
        for widget in self.analisys_frame2.winfo_children():
            widget.destroy()
        
        data = self.analysis.get_top_orders()  # Используем метод из импортированного класса
        if not data:
            tk.Label(self.analisys_frame2, text="Нет данных для построения графика", 
                    font=('Arial', 12), fg='red').pack(pady=50)
            return
        
        # Создаем DataFrame
        df = pd.DataFrame(data, columns=['ID заказа', 'Сумма заказа', 'Клиент'])
        
        # Создаем фигуру matplotlib
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Строим график
        df.plot(x='Клиент', y='Сумма заказа', kind='bar', ax=ax, color='skyblue')
        ax.set_title('ТОП 5 заказов по клиентам', fontsize=14, fontweight='bold')
        ax.set_xlabel('Клиент', fontsize=12)
        ax.set_ylabel('Сумма заказа (руб.)', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        
        # Добавляем подписи значений на столбцах
        for i, v in enumerate(df['Сумма заказа']):
            ax.text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')
        
        fig.tight_layout()
        
        # Встраиваем график в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.analisys_frame2)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Добавляем кнопку для обновления
        refresh_btn = tk.Button(self.analisys_frame2, text="Обновить график", 
                               command=self.plot_top_orders, bg='lightblue')
        refresh_btn.pack(pady=5)

    def plot_orders_by_date(self):
        """Строит график заказов по датам и отображает в analisys_frame2"""
        # Очищаем предыдущий график
        for widget in self.analisys_frame2.winfo_children():
            widget.destroy()
        
        data = self.dates_analysis.get_orders_dates()
        if not data:
            tk.Label(self.analisys_frame2, text="Нет данных для построения графика", 
                    font=('Arial', 12), fg='red').pack(pady=50)
            return
        
        try:
            # Создаем списки для данных
            dates = []
            totals = []
            
            for date_str, total in data:
                try:
                    # Пытаемся преобразовать дату
                    if isinstance(date_str, str):
                        dates.append(pd.to_datetime(date_str))
                    else:
                        dates.append(date_str)
                    totals.append(float(total))
                except:
                    continue  # Пропускаем некорректные данные
            
            if not dates:
                tk.Label(self.analisys_frame2, text="Нет корректных данных для построения графика", 
                        font=('Arial', 12), fg='red').pack(pady=50)
                return
            
            # Создаем фигуру matplotlib
            fig = Figure(figsize=(12, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # Строим линейный график
            ax.plot(dates, totals, marker='o', linestyle='-', 
                    color='green', linewidth=2, markersize=6)
            
            ax.set_title('Сумма заказов по датам', fontsize=14, fontweight='bold')
            ax.set_xlabel('Дата заказа', fontsize=12)
            ax.set_ylabel('Сумма заказов (руб.)', fontsize=12)
            
            # Форматируем даты на оси X
            fig.autofmt_xdate(rotation=45)
            
            # Добавляем сетку
            ax.grid(True, alpha=0.3)
            
            # Добавляем подписи значений на точках
            for i, (date, total) in enumerate(zip(dates, totals)):
                ax.annotate(f'{total:.2f}', 
                        xy=(date, total),
                        xytext=(0, 10),
                        textcoords='offset points',
                        ha='center',
                        va='bottom',
                        fontweight='bold',
                        fontsize=8)
            
            fig.tight_layout()
            
            # Встраиваем график в Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.analisys_frame2)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Добавляем кнопку для обновления
            refresh_btn = tk.Button(self.analisys_frame2, text="Обновить график", 
                                command=self.plot_orders_by_date, bg='lightblue')
            refresh_btn.pack(pady=5)
            
        except Exception as e:
            tk.Label(self.analisys_frame2, 
                    text=f"Ошибка при построении графика: {str(e)}", 
                    font=('Arial', 12), fg='red').pack(pady=50)
            print(f"Ошибка в plot_orders_by_date: {e}")
    def create_analisys_tab(self):
        # Создаем фрейм для размещения кнопок анализа
        form_frame2 = ttk.LabelFrame(self.parent, text="Выбор анализа данных")
        form_frame2.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Кнопка ТОП 5 заказов
        button_top = tk.Button(form_frame2, text='ТОП 5 заказов', pady=5, 
                              bg='lightgreen', command=self.plot_top_orders)
        button_top.grid(row=0, column=0, columnspan=2, padx=5)

        # Кнопка Заказы по датам
        button_date = tk.Button(form_frame2, text='Заказы по датам', pady=5, 
                               bg='lightgreen', command=self.plot_orders_by_date)
        button_date.grid(row=0, column=2, columnspan=2, padx=5)

        button_gr = tk.Button(form_frame2, text='Заказы по городам', pady=5, 
                             bg='lightgreen', command=self.plot_city_goods_graph) 
        button_gr.grid(row=0, column=4, columnspan=2, padx=5)

        # Создаем фрейм для вывода анализа данных
        self.analisys_frame2 = ttk.LabelFrame(self.parent, text="Вывод анализа данных")
        self.analisys_frame2.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        # Настройка веса для растягивания
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.analisys_frame2.grid_rowconfigure(0, weight=1)
        self.analisys_frame2.grid_columnconfigure(0, weight=1)
        
        # Изначальное сообщение
        tk.Label(self.analisys_frame2, text="Выберите тип анализа данных выше", 
                font=('Arial', 12), fg='gray').pack(expand=True)