# -*- coding: utf-8 -*-
"""Программа-клиент"""

import sys
import json
import logging
import socket
import time
import argparse
import log.client_log_config
from decorators import log
from errors import MissingData
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message

LOGGER_CLIENT = logging.getLogger('client')


@log
def request_for_presence(account_name='Guest'):
    '''Функция генерирует запрос о присутствии клиента'''
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOGGER_CLIENT.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return message


@log
def response_processing(message):
    '''Функция разбирает ответ сервера'''
    LOGGER_CLIENT.debug(f'Обработка сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise MissingData


@log
def arg_parser():
    """"""
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    my_parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return my_parser


def main():
    '''Загрузка параметров командной строки'''
    parser = arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    address = namespace.addr
    port = namespace.port

    # Проверка номера порта
    if not 1023 < port < 65536:
        LOGGER_CLIENT.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    LOGGER_CLIENT.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {address} , порт: {port}')

    # Инициализация сокета и обмен

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((address, port))
        message_to_server = request_for_presence()
        send_message(transport, message_to_server)
        answer = response_processing(get_message(transport))
        LOGGER_CLIENT.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        LOGGER_CLIENT.error('Не удалось декодировать полученную Json строку.')
    except MissingData as missing_error:
        LOGGER_CLIENT.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
    except ConnectionRefusedError:
        LOGGER_CLIENT.critical(f'Не удалось подключиться к серверу {address}:{port}, '
                               f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
