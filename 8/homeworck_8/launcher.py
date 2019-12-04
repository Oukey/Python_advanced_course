# -*- coding: utf-8 -*-
"""Лаунчер"""

import subprocess

PROCESS = []

while True:
    ACT = input(
        'Меню действий: q - выход; s - запуск сервера и клиентов; x - закрыть все окна. Введите команду ')

    if ACT == 'q':
        break
    elif ACT == 's':
        PROCESS.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

        for _ in range(2):
            PROCESS.append(
                subprocess.Popen('python client.py - m send', creationflags=subprocess.CREATE_NEW_CONSOLE))

        for _ in range(3):
            PROCESS.append(subprocess.Popen('python client.py -m listen',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACT == 'x':
        while PROCESS:
            TO_COMPLETE = PROCESS.pop()
            TO_COMPLETE.kill()
