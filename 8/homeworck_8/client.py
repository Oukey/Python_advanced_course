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
from errors import MissingData, ServerError
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, ERROR, MESSAGE, TEXT_MESSAGE,\
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, SENDER
from common.utils import get_message, send_message

LOGGER_CLIENT = logging.getLogger('client')


@log
def request_for_presence(message):
    '''Функция генерирует запрос о присутствии клиента'''
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and TEXT_MESSAGE in message:
        print(f'Получено сообщение от пользователя {message[SENDER]}: \n {message[TEXT_MESSAGE]}')
        LOGGER_CLIENT.info(f'Получено сообщение от пользователя {message[SENDER]}: \n {message[TEXT_MESSAGE]}')
    else:
        LOGGER_CLIENT.error(f'Получено неккоректное сообщение от сервера {message}')


@log
def message_processing(sock, account_name='Guest'):
    """Запроса и возврата сообщения"""
    message = input(
        'Введите сообщение для отправки или \'~\' для завершения работы: ')
    if message == '~':
        sock.close()
        LOGGER_CLIENT.info('Завершение работы по команде пользователя.')
        print('До скорых встреч!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        TEXT_MESSAGE: message
    }
    LOGGER_CLIENT.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def request_presence(account_name='Guest'):
    """Функция запрашивает присутствие клиента"""
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOGGER_CLIENT.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def server_response_processing(message):
    """Функция обработки ответа от сервера"""
    LOGGER_CLIENT.debug(f'Сообщение-приветствие от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise MissingData(RESPONSE)


@log
def arg_parser():
    """Метод обработки аргументов командной строки"""
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    my_parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    my_parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = my_parser.parse_args(sys.argv[1:])
    address = namespace.addr
    port = namespace.port
    client_mode = namespace.mode

    # проверка корректности
    if not 1023 < port < 65536:
        LOGGER_CLIENT.critical(
            f'Попытка запуска клиента с неккоректным номером порта: {port}.')
        sys.exit(1)

    # Проверим режима работы
    if client_mode not in ('listen', 'send'):
        LOGGER_CLIENT.critical(f'Указан недопустимый режим работы {client_mode}, доступные режимы: listen , send')
        sys.exit(1)

    return address, port, client_mode


def main():
    """Загружаем параметы коммандной строки"""
    server_address, server_port, client_mode = arg_parser()

    LOGGER_CLIENT.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
        f'порт: {server_port}, режим работы: {client_mode}')

    # Инициализация сокета и сообщение серверу о нашем появлении
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, request_presence())
        answer = server_response_processing(get_message(transport))
        LOGGER_CLIENT.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        LOGGER_CLIENT.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        LOGGER_CLIENT.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except MissingData as missing_error:
        LOGGER_CLIENT.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        LOGGER_CLIENT.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    send_message(transport, message_processing(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER_CLIENT.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    request_for_presence(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER_CLIENT.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
