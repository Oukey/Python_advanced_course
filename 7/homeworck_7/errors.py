# -*- coding: utf-8 -*-
"""Модуль описания ошибок"""


class ErrorData(Exception):
    """Класс обработки некорректных данных от сокета"""

    def __str__(self):
        return 'Принято неккоректное сообщение от удаленного компьютера.'


class ErrorType(Exception):
    """Класс обработки ошибки типа, когда агрумент не является словарем"""

    def __str__(self):
        return 'Аргумент функции не является словарем!'


class MissingData(Exception):
    """Класс обработки отсутствия обязательных полей в принятом словаре"""
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отсутствует обязательное поле {self.missing_field}.'


class ServerError(Exception):
    """Ошибка сервера"""
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text
