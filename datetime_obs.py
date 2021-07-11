from main import *
from enc_obs import enc_aes, dec_aes

import os
import datetime
from time import sleep


__version__ = '1.2.1'


def greeting(generic_key):   # Greating Depending On Date Time
    """ Фунция вывода приветствия в зависимости от времени суток """
    def template_greeting(times_of_day):
        if os.path.exists(FILE_USER_NAME) is False:  # Создание файла с именем
            name = input(YELLOW + '\n -- Your nickname: ' + DEFAULT_COLOR)
            enc_aes(FILE_USER_NAME, name, generic_key)
        else:  # Чтение из файла с именем и вывод в консоль
            name = dec_aes(FILE_USER_NAME, generic_key)
        print('\n', GREEN, times_of_day, name, DEFAULT_COLOR)

    hms = datetime.datetime.today()
    time_now = hms.hour * 3600 + hms.minute * 60 + hms.second  # Время в секундах
    if 14400 <= time_now < 43200:  # Condition morning
        template_greeting('Good morning,')
    elif 43200 <= time_now < 61200:  # Condition day
        template_greeting('Good afternoon,')
    elif 61200 <= time_now <= 86399:  # Condition evening
        template_greeting('Good evening,')
    elif 0 <= time_now < 14400:  # Condition night
        template_greeting('Good night,')
    sleep(.5)
