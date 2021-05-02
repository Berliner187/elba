import os
import datetime
# Проприетарный модуль шифрования
from enc_obs import enc_data, dec_data
from main import *


__version__ = '1.0.2'


def greeting(master_password):   # Greating Depending On Date Time
    """ Фунция вывода приветствия в зависимости от времени суток """
    def get_name():
        if os.path.exists(FILE_USER_NAME) == bool(False):  # Создание файла с именем
            with open(FILE_USER_NAME, "w") as self_name:
                name = input(yellow + '\n -- Your name or nickname: ' + DEFAULT_COLOR)
                enc_name = enc_data(name, master_password)
                self_name.write(enc_name)
                self_name.close()
                return name
        else:  # Чтение из файла с именем и вывод в консоль
            with open(FILE_USER_NAME, "r") as self_name:
                dec_name = self_name.readline()
                name = dec_data(dec_name, master_password)
                return name

    def template_greeting(times_of_day):
        print('\n', GREEN, times_of_day, get_name(), DEFAULT_COLOR)

    hms = datetime.datetime.today()
    hours_to_secunds = hms.hour * 3600 + hms.minute * 60 + hms.second
    time_now = hours_to_secunds    # Время в секундах
    if 14400 <= time_now < 43200:  # Condition morning
        template_greeting('Good modring,')
    elif 43200 <= time_now < 61200:  # Condition day
        template_greeting('Good afternoon,')
    elif 61200 <= time_now <= 86399:  # Condition evening
        template_greeting('Good evening,')
    elif 86399 <= time_now < 14400:  # Condition night
        template_greeting('Good night,')


greeting('kozak022')
