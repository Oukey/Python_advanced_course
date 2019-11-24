# -*- coding: utf-8 -*-
"""Тестирование программы-сервера"""

import unittest
import time
import server as srv


class TestServer(unittest.TestCase):
    """Класс тестов модуля server"""

    normal = {'response': 200}

    error = {
        'respond_default_ip_address': 400,
        'error': 'Bad Request'
    }

    def test_norm(self):
        """Тест функции обработки сервером сообщения от клиента когда все нормульно"""
        self.assertEqual(srv.process_client_message({
            'action': 'presence',
            'time': time.time(),
            'user': {'account_name': 'Guest'}
        }), self.normal)

    def test_error_action_0(self):
        """Тест обработки сообщения если не указано действие"""
        self.assertEqual(srv.process_client_message({
            'time': time.time(),
            'user': {'account_name': 'Guest'}
        }), self.error)

    def test_error_action_1(self):
        """Тест обработки сообщения если действие не известно"""
        self.assertEqual(srv.process_client_message({
            'action': 'null',
            'time': time.time(),
            'user': {'account_name': 'Guest'}
        }), self.error)

    def test_error_action_2(self):
        """Тест обработки сообщения если не указан юзер"""
        self.assertEqual(srv.process_client_message({
            'action': 'presence',
            'time': time.time(),
        }), self.error)

    def test_error_action_3(self):
        """Тест обработки сообщения если не корректное имя юзера"""
        self.assertEqual(srv.process_client_message({
            'action': 'null',
            'time': time.time(),
            'user': {'account_name': 'Tom'}
        }), self.error)


if __name__ == '__main__':
    unittest.main()
