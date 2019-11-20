# -*- coding: utf-8 -*-
"""Тестирование утилит"""

import unittest
import json


class Socket:
    """Вспомогательный класс для работы с сокетом. Принимает словарь"""

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_msg = 0
        self.received_msg = 0

    def sending(self, message):
        """Тестовая функция отправки"""
        json_message = json.dumps(self.test_dict)
        self.encoded_msg = json_message.encode('utf-8')
        self.received_msg = message

    def receive(self):
        """Тестовая функция получения"""
        return json.dumps(self.test_dict).encode('utf-8')


class TestUtils(unittest.TestCase):
    """Класс тесто в модуля utils"""

    normal = {'response': 200}
    error = {
        'respond_default_ip_address': 400,
        'error': 'Bad Request'}
    test_msg = {
        'action': 'presence',
        'time': 0.1,
        'user': {
            'account_name': 'test_test'}
    }

    def test_send_msg(self):
        """Тест отправки"""
        socket = Socket(self.test_msg)
        self.assertEqual(socket.encoded_msg, socket.received_msg)


if __name__ == '__main__':
    unittest.main()
