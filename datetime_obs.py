# -*- coding: UTF-8 -*-

"""
   Модуль времени
"""

from main import *

import security_obs
import logo_obs

import os
import shutil
import datetime
from time import sleep


__version__ = '0.10-02'

SLEEPER_WAIT = .022     # Константа задержки вывода


def greeting(generic_key):   # Greeting Depending On Date Time
    """ Функция отображения приветствия """
    def template_greeting(times_of_day):
        if os.path.exists(FILE_USER_NAME) is False:  # Создание файла с именем
            system_action('clear')
            print(ACCENT_3)
            logo_obs.iterate_over_characters(' Enter your nickname', SLEEPER_WAIT)
            name = template_input(' Nickname:')
            security_obs.enc_aes(FILE_USER_NAME, name, generic_key)
        else:  # Чтение из файла с именем и вывод в консоль
            name = security_obs.dec_aes(FILE_USER_NAME, generic_key)
        lines = [
            f'{times_of_day} {name}'
        ]
        logo_obs.wait_effect(lines, SLEEPER_WAIT)
        sleep(SLEEPER_WAIT)
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
    sleep(.3)
