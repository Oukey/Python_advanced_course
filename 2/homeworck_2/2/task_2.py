# -*- coding: utf-8 -*-
'Задание №1. Закрепление работы с файлами json'

import json


def write_order_to_json(item, quantity, price, buyer, date):
    "Функция записи данных в файл orders.json"
    with open('orders.json', encoding='utf-8') as f_l:
        data = {
            "item": item,
            "quantity": int(quantity),
            "price": int(price),
            "buyer": buyer,
            "date": date
        }
        with open('orders.json', 'r') as file:
            result = json.load(file)
        with open('orders.json', 'w') as file:
            result['orders'].append(data)
            json.dump(result, file, indent=4)


write_order_to_json('bass', '1', '14500', 'No_name', '11.11.2019')
write_order_to_json('booster', '1', '9700', 'Che', '11.11.2019')
