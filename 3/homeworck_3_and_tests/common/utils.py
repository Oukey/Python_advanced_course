# -*- coding: utf-8 -*-
"""Утилиты"""

import json
from common.variables import MAX_PACKAGE_LENGTH, ENCODING


def get_message(client):
    '''
    Утилита приема и декодирования сообщения
    принимает байты выдает словарь,
    если принято что-то другое отдает ошибку значения
    '''

    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock, message):
    '''
    Утилита кодирования и отправления сообщения
    принимает словарь и отправляет его
    '''

    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    sock.send(encoded_message)
