# -*- coding: utf-8 -*-
"""Программа - сервер"""

import socket
import sys
import logging
import argparse
import select
import time
import log.server_log_config
from errors import ErrorData
from decorators import log
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, SENDER,\
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, TEXT_MESSAGE
from common.utils import get_message, send_message

LOGGER_SERVER = logging.getLogger('server')


@log
def process_client_message(message, message_list, client):
    '''
    Обработчик сообщений от клиентов,
    принимает словарь - сообщение от клиента, проверяет корректность,
    возвращает словарь - ответ для клиента
    '''
    # Обработка сообщения о присутствии
    LOGGER_SERVER.debug(f'Обработка сообщения от клиента: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    # Обработка сообщения
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and TEXT_MESSAGE in message:
        message_list.append((message[ACCOUNT_NAME], message[TEXT_MESSAGE]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad request'
        })
        return


@log
def arg_parser():
    """Анализ аргументов коммандной строки"""
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    my_parser.add_argument('-a', default='', nargs='?')
    namespace = my_parser.parse_args(sys.argv[1:])
    address = namespace.a
    port = namespace.p

    # проверка корректности
    if not 1023 < port < 65536:
        LOGGER_SERVER.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return address, port


def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаем значения по умолчанию.
    '''
    address, port = arg_parser()
    LOGGER_SERVER.info(
        f'Сервер запущен. Порт подключения: {port}, адрес: {address}.')

    # Подготовка сокет
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((address, port))
    my_socket.settimeout(1)

    clients_list, message_list = [], []
    r_data, s_data, error_list = [], [], []

    # Прослушивание порта
    my_socket.listen(MAX_CONNECTIONS)

    # основной цикл
    while True:
        try:
            client, address = my_socket.accept()
        except OSError:
            pass
        else:
            LOGGER_SERVER.info(f'Установлено соединение с ПК {address}')
            clients_list.append(client)

        # Проверка ожидающих клиентов
        try:
            if clients_list:
                r_data, s_data, error_list = select.select(
                    clients_list, clients_list, [], 0)
        except OSError:
            pass
        # Прием и обработка сообщений, ошибок
        if r_data:
            for client_message in r_data:
                try:
                    process_client_message(
                        get_message(client_message), message_list, client_message)
                except BaseException:
                    LOGGER_SERVER.info(f'Клиент {client_message.getpeername()} отключился')
                    clients_list.remove(client_message)

        # Отправка сообщения ожидающим коиентам
        if message_list and s_data:
            message = {
                ACTION: MESSAGE,
                SENDER: message_list[0][0],
                TIME: time.time(),
                TEXT_MESSAGE: message_list[0][1]
            }
            del message_list[0]
            for waiting_client in s_data:
                try:
                    send_message(waiting_client, message)
                except BaseException:
                    LOGGER_SERVER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients_list.remove(waiting_client)


if __name__ == '__main__':
    main()
