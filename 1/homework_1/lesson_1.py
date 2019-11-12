# -*- coding: utf-8 -*-
"""Модуль для задач №1-4"""

# Задание №1
WORD = ['разработка', 'сокет', 'декоратор']
for i in WORD:
    print(i, type(i))

for i in WORD:
    print('{}: '.format(i))
    e = bytes(i.encode('utf-16'))
    print('UTF-16 ', e)
    e = bytes(i.encode('utf-8'))
    print('UTF-8 ', e)
    print(type(e))

# Задание №2
print('-' * 40)
WORD_1 = [b'class', b'function', b'method']
for i in WORD_1:
    print(
        'Тип: {}, содержимое: {}, длинна: {}'.format(
            type(i),
            i,
            len(i)))

# Задание №3
print('-' * 40)
WORD_2 = ['attribute', 'класс', 'функция', 'type']
RESULT_LIST = []

for i in WORD_2:
    try:
        # i.encode('ascii')
        bytes(i, 'ascii')
    except UnicodeEncodeError:
        RESULT_LIST.append(i)
print('Эти слова нельзя записать в байтовом типе с кодировкой ascii ', RESULT_LIST)


# Задание №4
print('-' * 40)
WORD_3 = ['разработка', 'администратирование', 'protocol', 'standard']
for i in range(len(WORD_3)):
    WORD_3[i] = WORD_3[i].encode('utf-8')
print(WORD_3)

for i in range(len(WORD_3)):
    WORD_3[i] = WORD_3[i].decode('utf-8')
print(WORD_3)

# Задание №5
print('-' * 40)
