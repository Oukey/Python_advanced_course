# -*- coding: utf-8 -*-
"""Программа - сервер"""

import socket
import sys
import json
import logging
import argparse
import log.server_log_config
from errors import ErrorData
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPOND_DEFAULT_IP_ADDRESS
from common.utils import get_message, send_message

LOGGER_SERVER = logging.getLogger('server')


def process_client_message(message):
    '''
    Обработчик сообщений от клиентов,
    принимает словарь - сообщение от клиента, проверяет корректность,
    возвращает словарь - ответ для клиента
    '''
    LOGGER_SERVER.debug(f'Обработка сообщения от клиента: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPOND_DEFAULT_IP_ADDRESS: 400,
        ERROR: 'Bad Request'
    }


def arg_parser():
    """Анализ аргументов коммандной строки"""
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    my_parser.add_argument('-a', default='', nargs='?')
    return my_parser


def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаем значения по умолчанию.
    '''

    my_parser = arg_parser()
    namespace = my_parser.parse_args(sys.argv[1:])
    address = namespace.a
    port = namespace.p

    # Проверка корректности
    if not 1023 < port < 65536:
        LOGGER_SERVER.critical(f'Запуск сервера с указанием неподходящего порта' f'{port}. '
                               f'Допустимые адреса с 1024 до 65535.')
        sys.exit(1)
    LOGGER_SERVER.info(f'Запущен сервер, порт для подключений: {port}, '
                       f'адрес с которого принимаются подключения: {address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')
    # Готовим сокет

    # Подготовка сокет
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((address, port))

    # Прослушивание порта
    my_socket.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = my_socket.accept()
        LOGGER_SERVER.info(f'Установлено соединение с ПК {address}')
        try:
            message_client = get_message(client)
            LOGGER_SERVER.debug(f'Получено сообщение {message_client}')
            response = process_client_message(message_client)
            LOGGER_SERVER.info(f'Создан ответ клиенту {response}')
            send_message(client, response)
            LOGGER_SERVER.debug(f'Закрытие соединения с клиентом: {address}')
            client.close()
        except json.JSONDecodeError:
            LOGGER_SERVER.error(f'Не удалось декодировать сообщение от клиента {address}. Закрытие соединения.')
            client.close()
        except ErrorData:
            LOGGER_SERVER.error(f'Приняты некорректные данные от клиента {address}. Закрытие соединения. ')
            client.close()


if __name__ == '__main__':
    main()
