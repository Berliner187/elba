#!/usr/bin/env python3
from main import *
import os
import sys
from memory_profiler import memory_usage


__version__ = '1.2.0'


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
    print(BLUE, "\n\n - Volume taken up by the program - \n", DEFAULT_COLOR)
    size_mod_cache = size_program = size_user_data = 0

    # Получение файлов программы
    file_type = 'obs.py'
    any_file = os.listdir('.')
    files = []
    for file in any_file:
        if file.endswith(file_type):
            files.append(file)
    files.append('main.py')

    # Получение веса кэша модулей
    cache = '.pyc'
    cache_modules = []
    direct = os.listdir('__pycache__/')
    for item in direct:
        if item.endswith(cache):
            cache_modules.append(item)
    for i in range(len(cache_modules)):
        size_mod_cache += os.path.getsize('__pycache__/' + cache_modules[i])

    # Вывод веса модулей и главной программы
    dic_with_files_program = {}
    for i in range(len(files)):
        size_program += os.path.getsize(files[i])
        dic_with_files_program[files[i]] = os.path.getsize(files[i]) * 8

    for file, size in dic_with_files_program.items():
        print("{0} --- {1}".format(size, file))

    # Получение размера пользовательских файлов
    for folder_with_resource in os.listdir(FOLDER_WITH_RESOURCES):
        for file in os.listdir(FOLDER_WITH_RESOURCES + folder_with_resource):
            size_user_data += os.path.getsize(FOLDER_WITH_RESOURCES + folder_with_resource + '/' + file)
    for folder_with_note in os.listdir(FOLDER_WITH_NOTES):
        for file in os.listdir(FOLDER_WITH_NOTES + folder_with_note):
            size_user_data += os.path.getsize(FOLDER_WITH_NOTES + folder_with_note + '/' + file)
    for file in os.listdir(FOLDER_WITH_DATA):
        size_user_data += os.path.getsize(FOLDER_WITH_DATA + file)

    size_logs = os.path.getsize(FILE_LOG)

    def to_another_unit_of_measurement(__size__):
        """ Округление и перевод в единицы измерения """
        if 2**20 < __size__:
            __size__ = round((__size__ / (2**20)), 2)
            user_measure = 'MiB'
        elif 2**10 < __size__ < 2**20:
            user_measure = 'KiB'
            __size__ = round((__size__ / (2**10)), 2)
        else:
            user_measure = 'B'
            __size__ = round(__size__, 2)

        return YELLOW + str(__size__) + ' ' + user_measure + DEFAULT_COLOR

    print('\n')

    program_in_ram = memory_usage()
    program_in_ram = program_in_ram[0] * 2**20

    total_data = size_program + size_mod_cache + size_user_data + size_logs
    data_to_print = {
        'The program occupies RAM ': to_another_unit_of_measurement(program_in_ram),
        'The log files too        ': to_another_unit_of_measurement(size_logs),
        'User files took          ': to_another_unit_of_measurement(size_user_data),
        'The program files took up': to_another_unit_of_measurement(size_program),
        'The program cache tok up ': to_another_unit_of_measurement(size_mod_cache),
        'The total program takes  ': to_another_unit_of_measurement(total_data)
    }
    for text, space_used in data_to_print.items():
        print("{0}: {1}".format(text, space_used))


size_all()
