#!/usr/bin/env python3
from main import *
import os


def size_all():
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

    def rounding(size):
        """ Округление в килобайты """
        return round((size / 2**10), 1)

    user_folder = "volare/"
    size_user_data = 0
    for item in os.listdir(user_folder):
        if item.endswith(".csv") or item.endswith(".dat"):
            size_user_data += os.path.getsize(user_folder + item)
    
    size_program += size_mod_cache  # Вычисление всего веса
    print('\n Данные пользователя заняли', YELLOW,
        size_user_data, 'Байт', DEFAULT_COLOR)
    print('\n Файлы программы заняли', YELLOW,
        rounding(size_program - size_mod_cache), 'Килобайт', DEFAULT_COLOR)
    print('\n Кэш модулей занял', YELLOW,
        rounding(size_mod_cache) , 'Килобайт', DEFAULT_COLOR)
    print('\n Итого весь проект занимает', YELLOW,
        rounding(size_program), 'Килобайт в ПЗУ \n', DEFAULT_COLOR)
