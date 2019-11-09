# -*- coding: utf-8 -*-
"""Модуль для пинга. Задача №5"""

import subprocess
import chardet


def ping(address):
    args = ['ping', address]
    ya_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    print(ya_ping)
    for line in ya_ping.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))


# Для яндекса
ping('yandex.ru')

# Для ютьюба
ping('youtube.com')

# Для всего
# SITE = input('Введите адрес ресурса: ')
# ping(SITE)
