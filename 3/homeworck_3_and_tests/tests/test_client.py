# -*- coding: utf-8 -*-
"""Тестирование программы-клиент"""

import unittest
import client as cl


class TestClient(unittest.TestCase):
    """Класс тестов модуля client"""

    def test_create_presence(self):
        """Тест функции генерации запроса о присутствии клиента"""
        result = cl.create_presence()
        self.assertIsInstance(result, dict)

    def test_response_processing(self):
        """Тест функции разбора отета от сервера"""
        self.assertEqual(cl.response_processing({'response': 200}), '200 : OK')


if __name__ == '__main__':
    unittest.main()
