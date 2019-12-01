# -*- coding: utf-8 -*-
"""Декораторы"""

import sys
import logging
import log.client_log_config
import log.server_log_config

# Определение модуля client/server:
if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(func):
    """Функция-декоратор"""
    def log_saver(*args, **kwargs):
        ret = func(*args, **kwargs)
        LOGGER.debug(f'Вызвана функция {func.__name__} c параметрами: {args}, {kwargs}. '
                     f'Из модуля: {func.__module__}')
        return ret
    return log_saver
