# -*- coding: utf-8 -*-
"""Модуль для работы с файлом"""

WORD = ['сетевое программирование', 'сокет', 'декоратор']

# Создание файла
with open('test_file.txt', 'wt') as f:
    for elem in WORD:
        f.write(str(elem) + '\n')

# Проверка кодировки файла
T_F = open('test_file.txt')
T_F.close()
print(type(T_F))

# Открытие и чтение файла
with open('test_file.txt', encoding='utf=8') as f:
    for line in f:
        print(line, end='')
