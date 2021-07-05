from main import *
from enc_obs import enc_aes, dec_aes

import os
import datetime


__version__ = '1.1.2'


def greeting(generic_key):   # Greating Depending On Date Time
    """ Фунция вывода приветствия в зависимости от времени суток """
    def get_name():
        if os.path.exists(FILE_USER_NAME) is False:  # Создание файла с именем
            name = input(YELLOW + '\n -- Your name or nickname: ' + DEFAULT_COLOR)
            enc_aes(FILE_USER_NAME, name, generic_key)
            return name
        else:  # Чтение из файла с именем и вывод в консоль
            name = dec_aes(FILE_USER_NAME, generic_key)
            return name

    def template_greeting(times_of_day):
        print('\n', GREEN, times_of_day, get_name(), DEFAULT_COLOR)

    hms = datetime.datetime.today()
    hours_to_seconds = hms.hour * 3600 + hms.minute * 60 + hms.second
    time_now = hours_to_seconds    # Время в секундах
    if 14400 <= time_now < 43200:  # Condition morning
        template_greeting('Good modring,')
    elif 43200 <= time_now < 61200:  # Condition day
        template_greeting('Good afternoon,')
    elif 61200 <= time_now <= 86399:  # Condition evening
        template_greeting('Good evening,')
    elif 86399 <= time_now < 14400:  # Condition night
        template_greeting('Good night,')
