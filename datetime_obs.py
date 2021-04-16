import datetime
import os
from enc_obs import enc_data, dec_data


yellow, blue, purple, green, mc, red = "\033[33m", "\033[36m", "\033[35m", "\033[32m", "\033[0m", "\033[31m"
main_folder = 'volare/'
file_self_name = main_folder + ".self_name.dat"  # Файл с именем (никнеймом)


def greeting(master_password):   # Greating Depending On Date Time
    """ Фунция вывода приветствия в зависимости от времени суток """
    def get_name():
        if os.path.exists(file_self_name) == bool(False):  # Создание файла с именем
            with open(file_self_name, "w") as self_name:
                name = input(yellow + '\n -- Your name or nickname: ' + mc)
                enc_name = enc_data(name, master_password)
                self_name.write(enc_name)
                self_name.close()
                return name
        else:  # Чтение из файла с именем и вывод в консоль
            with open(file_self_name, "r") as self_name:
                dec_name = self_name.readline()
                name = dec_data(dec_name, master_password)
                return name

    def template_greeting(times_of_day):
        print(green, times_of_day, get_name(), mc)

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
