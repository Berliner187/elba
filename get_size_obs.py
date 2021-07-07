#!/usr/bin/env python3
from main import *
import os
import sys
import json


__version__ = '1.1.3'


def get_versions():
    from change_password_obs import __version__ as change_password_ver
    from actions_with_password_obs import __version__ as actions_with_password_ver
    from datetime_obs import __version__ as datetime_ver
    from del_resource_obs import __version__ as del_resource_ver
    from enc_obs import __version__ as enc_ver
    from get_size_obs import __version__ as get_size_ver
    from logo_obs import __version__ as logo_ver
    from notes_obs import __version__ as notes_ver
    from update_obs import __version__ as update_ver
    from show_dec_data_obs import __version__ as show_dec_ver

    system_action("clear")
    print(GREEN, '\n  - Versions installed modules - \n', DEFAULT_COLOR)

    def template_version_module(module, version):
        print(YELLOW, version, GREEN, module, DEFAULT_COLOR)

    template_version_module('program', __version__)
    template_version_module('change_password_obs', change_password_ver)
    template_version_module('confirm_password_obs', actions_with_password_ver)
    template_version_module('datetime_obs', datetime_ver)
    template_version_module('del_resource_obs', del_resource_ver)
    template_version_module('enc_obs', enc_ver)
    template_version_module('get_size_obs', get_size_ver)
    template_version_module('logo_obs', logo_ver)
    template_version_module('notes_obs', notes_ver)
    template_version_module('update_obs', update_ver)
    template_version_module('show_dec_data_obs', show_dec_ver)


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

    size_program = 0
    for i in range(len(files)):
        size = os.path.getsize(files[i])
        print(size * 8, 'b', ' ----- ', files[i])
        size_program += size

    def rounding(__size__):
        """ Округление и перевод в килобайты """
        return round((__size__ / 2**10), 2)

    user_folder = FOLDER_WITH_DATA
    size_user_data = 0
    for item in os.listdir(user_folder):
        if item.endswith(".csv") or item.endswith(".dat") or item.endswith(".log"):
            size_user_data += os.path.getsize(user_folder + item)

    size_program += size_mod_cache  # Вычисление всего веса
    size_logs = os.path.getsize(user_folder + '.file.log')

    def to_another_measurement_system(some_data_size):
        if some_data_size > 2**10:
            some_data_size = rounding(some_data_size)
            user_measure = 'KiB'
        else:
            user_measure = 'B'
        return YELLOW + str(some_data_size) + ' ' + user_measure + DEFAULT_COLOR

    print('\n')

    total_data = size_program + size_user_data + os.path.getsize('get_size_obs.py') + size_logs
    dic = {
        'Occupied space in RAM ': to_another_measurement_system(36404),
        'Log-files occupied    ': to_another_measurement_system(size_logs),
        'User files occupied   ': to_another_measurement_system(size_user_data),
        'Files program occupied': to_another_measurement_system(size_program - size_mod_cache),
        'Cash modules occupied ': to_another_measurement_system(size_mod_cache),
        'Total program occupied': to_another_measurement_system(total_data)
    }
    for text, space in dic.items():
        print("{0}: {1}".format(text, space))
