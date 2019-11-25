# -*- coding: utf-8 -*-
"""Настройки для логов сервера"""

import sys
import os
import logging
import logging.handlers
import common.variables as var
sys.path.append('../')

# Создание формировщика логов:
FORMATTER_SERVER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка файла для записи согов
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

# Создание потоков вывода
STREAM = logging.StreamHandler(sys.stderr)
STREAM.setFormatter(FORMATTER_SERVER)
STREAM.setLevel(logging.ERROR)
FILE = logging.FileHandler(PATH, encoding='utf-8')
FILE.setFormatter(FORMATTER_SERVER)

# Создание и настройка регистратора
LOGGER = logging.getLogger('server')
LOGGER.addHandler(STREAM)
LOGGER.addHandler(FILE)
LOGGER.setLevel(var.LOGGING_LVL)

# Для отладки (работает при запуске скрипта)
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Информация для отладки')
    LOGGER.info('Информационное сообщение')
