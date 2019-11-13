# -*- coding: utf-8 -*-
"Задание №1. Закрепление работы с файлами csv"

import re
import csv

MAIN_DATA = []


def get_data():
    "Функция перебора файлов"
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []

    for i in range(1, 4):
        file_object = open('info_%s.txt' % i, encoding='utf-8')
        data = file_object.read()

        os_prod_reg = re.compile(r'Изготовитель системы:\s*\S*')
        os_prod_mas = os_prod_reg.findall(data)
        os_prod_list.append(os_prod_mas[0].split()[2])

        os_name_reg = re.compile(r'Windows\s\S*')
        os_name_mas = os_name_reg.findall(data)
        os_name_list.append(os_name_mas[0])

        os_code_reg = re.compile(r'Код продукта:\s*\S*')
        os_code_mas = os_code_reg.findall(data)
        os_code_list.append(os_code_mas[0].split()[2])

        # Тип системы
        os_type_reg = re.compile(r'Тип системы:\s*\S*')
        os_type_mas = os_type_reg.findall(data)
        os_type_list.append(os_type_mas[0].split()[2])

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    MAIN_DATA.append(headers)

    cout = 1
    for i in range(0, 3):
        row_data = []
        row_data.append(cout)
        row_data.append(os_prod_list[i])
        row_data.append(os_name_list[i])
        row_data.append(os_code_list[i])
        row_data.append(os_type_list[i])
        MAIN_DATA.append(row_data)
        cout += 1


def write_to_csv(_file):
    "Функция записи данных"
    get_data()
    with open(_file, 'w') as f:
        writer = csv.writer(f)
        for row in MAIN_DATA:
            writer.writerow(row)


write_to_csv('result.csv')
