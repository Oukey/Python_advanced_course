# -*- coding: utf-8 -*-
"""Настройки для логив клиента"""

import sys
import os
import logging
import common.variables as var
sys.path.append('../')

# Создание формировщика логов:
FORMATTER_CLIENT = logging.Formatter('%(asctime)-22s %(levelname)-8s %(filename)-13s %(message)s')

# Подготовка файла для записи согов
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

# Создание потоков вывода
STREAM = logging.StreamHandler(sys.stderr)
STREAM.setFormatter(FORMATTER_CLIENT)
STREAM.setLevel(logging.ERROR)
FILE = logging.FileHandler(PATH, encoding='utf-8')
FILE.setFormatter(FORMATTER_CLIENT)

# Создание и настройка регистратора
LOGGER = logging.getLogger('client')
LOGGER.addHandler(STREAM)
LOGGER.addHandler(FILE)
LOGGER.setLevel(var.LOGGING_LVL)

# Для отладки (работает при запуске скрипта)
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Информация для отладки')
    LOGGER.info('Информационное сообщение')
