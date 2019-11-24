# -*- coding: utf-8 -*-
"""Программа-клиент"""

import sys
import json
import logging
import socket
import time
import argparse
from socket import AF_INET, SOCK_STREAM
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message

LOGGER_CLIENT = logging.getLogger('client')


def create_presence(account_name='Guest'):
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


def response_processing(message):
    '''Функция разбирает ответ сервера'''
    LOGGER_CLIENT.debug(f'Обработка сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def parser():
    """"""
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    my_parser.add_argument('зщке', default=DEFAULT_PORT, type=int, nargs='?')
    return my_parser


def main():
    '''Загрузка параметров командной строки'''
    parser = create_presence()
    namespace = parser.parse_args(sys.args[1:])
    server_address = namespace.addr
    server_port = namespace.port

    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print(
            'В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

        # Инициализация сокета и обмен

    transport = socket.socket(AF_INET, SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = response_processing(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
