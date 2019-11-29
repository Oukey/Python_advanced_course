# -*- coding: utf-8 -*-
"""Тестирование программы-клиент"""

import unittest
import client as cl


class TestClient(unittest.TestCase):
    """Класс тестов модуля client"""

    def test_create_presence_0(self):
        """Тест функции генерации запроса о присутствии клиента"""
        request = cl.request_for_presence()
        self.assertIsInstance(request, dict)

    def test_create_presence_1(self):
        """Тест функции генерации запроса о присутствии клиента"""
        request = cl.request_for_presence()
        request['time'] = 2.2
        self.assertEqual(request, {
            'action': 'presence',
            'time': 2.2,
            'user': {
                'account_name': 'Guest'}
        })

    def test_create_presence_2(self):
        """Тест функции генерации запроса о присутствии клиента"""
        request = cl.request_for_presence('Tom')
        request['time'] = 2.2
        self.assertEqual(request, {
            'action': 'presence',
            'time': 2.2,
            'user': {
                'account_name': 'Tom'}
        })

    def test_response_processing_0(self):
        """Тест функции разбора отета от сервера когда все хорошо"""
        self.assertEqual(cl.response_processing({'response': 200}), '200 : OK')

    def test_response_processing_1(self):
        """Тест функции обработки ответа сервера когда не все хорошо"""
        self.assertEqual(cl.response_processing(
            {'response': 400, 'error': 'Bad Request'}), '400 : Bad Request')


if __name__ == '__main__':
    unittest.main()
