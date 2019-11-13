# -*- coding: utf-8 -*-
"Задание №1. Закрепление работы с файлами ​ yaml"

import yaml


data = {
    'number_items': 4,
    'name': [
        'rack',
        'bracket',
        'speakers',
        'tuner'],
    'price': {
        'rack': '10$',
        'bracket': '1200₽',
        'speakers': '17€',
        'tuner': '6¥'}}

with open('file.yaml', 'w', encoding='utf-8') as file_in:
    yaml.dump(data, file_in, default_flow_style=False, allow_unicode=True)

with open("file.yaml", 'r', encoding='utf-8') as file_out:
    result = yaml.load(file_out)

# if data == result:
#     print('Успешно')
