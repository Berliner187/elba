# -*- coding: UTF-8 -*-

"""
   Модуль вывода приветсвия при старте программы
"""

from main import *
from enc_obs import enc_aes, dec_aes
from logo_obs import wait_effect

import os
import shutil
import datetime
from time import sleep


__version__ = '1.3.4'


def greeting(generic_key):   # Greating Depending On Date Time
    """ Фунция вывода приветствия юзера """
    def template_greeting(times_of_day):
        if os.path.exists(FILE_USER_NAME) is False:  # Создание файла с именем
            message_about_enter_nickname = [BLUE, '\n Enter your nickname']
            wait_effect(message_about_enter_nickname, 0.025)
            name = input(YELLOW + '\n - Nickname: ' + DEFAULT_COLOR)
            enc_aes(FILE_USER_NAME, name, generic_key)
        else:  # Чтение из файла с именем и вывод в консоль
            name = dec_aes(FILE_USER_NAME, generic_key)
        lines = [
            GREEN, times_of_day + ' ' + name,
            DEFAULT_COLOR
        ]
        wait_effect(lines, 0.001)
    hms = datetime.datetime.today()
    time_now = hms.hour * 3600 + hms.minute * 60 + hms.second  # Время в секундах
    if 14400 <= time_now < 43200:
        template_greeting('Good morning,')
    elif 43200 <= time_now < 61200:
        template_greeting('Good afternoon,')
    elif 61200 <= time_now <= 86399:
        template_greeting('Good evening,')
    elif 0 <= time_now < 14400:
        template_greeting('Good night,')
    sleep(.5)
