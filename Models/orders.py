class Orders:
    def __init__(self, order_id, customer_name, items, total_price, order_date=None, status='новый'):
        """
        Конструктор класса Orders с поддержкой нескольких позиций.

        :param order_id: ID заказа
        :param customer_name: Имя клиента
        :param items: Список товаров в формате [(naim, price, quantity, item_total), ...]
        :param total_price: Общая сумма заказа
        :param order_date: Дата заказа
        :param status: Статус заказа
        """
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = items  # Список товаров
        self.total_price = total_price
        self.order_date = order_date
        self.status = status

    def tocsv(self):
        # Сохраняем все позиции в одной строке через разделитель |
        items_str = '|'.join([f"{naim},{price},{quantity},{item_total}" for naim, price, quantity, item_total in self.items])
        return f"{self.order_id};{self.customer_name};{items_str};{self.total_price};{self.status}"
        
    def get_order_info(self):
        info = f'Заказ №: {self.order_id}\n'
        info += f'Клиент: {self.customer_name}\n'
        info += f'Статус: {self.status}\n'
        info += f'Общая сумма: {self.total_price}\n\n'
        info += 'Позиции:\n'
        
        for i, (naim, price, quantity, item_total) in enumerate(self.items, 1):
            info += f"{i}. {naim} - {price} руб. x {quantity} = {item_total} руб.\n"
        
        return info
    
    def __str__(self):
        return f"Order#{self.order_id} ({self.customer_name}, {len(self.items)} позиций, {self.total_price} руб.)"