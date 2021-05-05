#!/usr/bin/env python3
from main import *
import os


__version__ = 'v1.0.3'


def size_all():
    """ Получении информации о занимаемой памяти в ОЗУ """
    print(BLUE, "\n\n - Объем, занимаемый программой - ", DEFAULT_COLOR)
    size_mod_cache = 0
    cache = '.pyc'
    file_type = '.py'    # Модули заканчиваются на *obs.py
    any_file = os.listdir('.')  # Поиск в текущей папке
    files = []    # Массив для установленных модулей
    for file in any_file:   # Итерация модулей
        if file.endswith(file_type):
            files.append(file)

    cache_modules = []
    direct = os.listdir('__pycache__/')
    for item in direct:
        if item.endswith(cache):
            cache_modules.append(item)

    for i in range(len(cache_modules)):
        size_mod_cache += os.path.getsize('__pycache__/' + cache_modules[i])

    print('\n')

    size_program = 0
    for i in range(len(files)):
        size = os.path.getsize(files[i])
        print(size * 8, 'b', ' ----- ', files[i])
        size_program += size

    size_program -= os.path.getsize('get_size_obs.py')

    print('\n Максимальный объем выделенной памяти в ОЗУ для программы:',
          33684 / 2**10,
          'Килобайт')

    def rounding(__size__):
        """ Округление и перевод в килобайты """
        return round((__size__ / 2**10), 2)

    user_folder = FOLDER_WITH_DATA
    size_user_data = 0
    for item in os.listdir(user_folder):
        if item.endswith(".csv") or item.endswith(".dat"):
            size_user_data += os.path.getsize(user_folder + item)

    size_program += size_mod_cache  # Вычисление всего веса

    def template_output(text, value, measure):
        """ Шаблон вывода информации """
        print('\n ', text, YELLOW, value, measure, DEFAULT_COLOR)

    if size_user_data > 2**10:
        size_user_data /= 2**10
        size_user_data = round(size_user_data, 2)
        user_measure = 'Килобайт'
    else:
        user_measure = 'Байт'

    total_data = size_program + size_user_data + os.path.getsize('get_size_obs.py')
    template_output('Данные пользователя заняли', size_user_data, user_measure)
    template_output('Файлы программы заняли', rounding(size_program - size_mod_cache), 'Килобайт')
    template_output('Кэш модулей занял', rounding(size_mod_cache), 'Килобайт')
    template_output('Итого весь проект занимает', rounding(total_data), 'Килобайт в ПЗУ')
