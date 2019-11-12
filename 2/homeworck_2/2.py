#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
"""
import datetime
import json
import os


def write_order_to_json(item, quantity, price, buyer, date):
    data = {
        "item": item,
        "quantity": int(quantity),
        "price": int(price),
        "buyer": buyer,
        "date": date
    }

    with open(os.path.join('assets', 'orders.json'), 'r') as file:
        json_data = json.load(file)

        print(json_data)
    with open(os.path.join('assets', 'orders.json'), 'w') as file:
        json_data['orders'].append(data)

        print(json_data)
        json.dump(json_data, file, indent=4)

    print('Файл создан')


write_order_to_json('Tuxedo', 12, 477, 'Sherlock', str(datetime.datetime.now()))
write_order_to_json('Chair', 3, 200, 'Bill', str(datetime.datetime.now()))
write_order_to_json('MacBook', 12, 1500, 'Harry', str(datetime.datetime.now()))
write_order_to_json('Phone', 12, 500, 'Sergio', str(datetime.datetime.now()))
write_order_to_json('Ball', 12, 100, 'Stephanie', str(datetime.datetime.now()))