# -*- coding: UTF-8 -*-

"""
   Модуль вывода приветсвия при старте программы
"""

from main import *
import enc_obs
import logo_obs

import os
import shutil
import datetime
from time import sleep


__version__ = 'P8.6_M1.0'

SLEEPER_WAIT = .02     # Ожидание вывода никнейма


def greeting(generic_key):   # Greeting Depending On Date Time
    """ Фунция вывода приветствия юзера """
    def template_greeting(times_of_day):
        if os.path.exists(FILE_USER_NAME) is False:  # Создание файла с именем
            system_action('clear')
            message_about_enter_nickname = [ACCENT_3, '\n Enter your nickname']
            logo_obs.wait_effect(message_about_enter_nickname, SLEEPER_WAIT)
            name = input(ACCENT_1 + '\n - Nickname: ' + ACCENT_4)
            enc_obs.enc_aes(FILE_USER_NAME, name, generic_key)
        else:  # Чтение из файла с именем и вывод в консоль
            name = enc_obs.dec_aes(FILE_USER_NAME, generic_key)
        lines = [
            f'{ACCENT_1} '
            f'{times_of_day} {name}'
            f'{ACCENT_4}'
        ]
        logo_obs.wait_effect(lines, SLEEPER_WAIT)
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
    sleep(.4)
