#!/usr/bin/env python3
from main import *
import os
import sys
from memory_profiler import memory_usage


__version__ = '2.0.3'


def get_versions():
    from main import __version__ as elba_v
    from change_password_obs import __version__ as change_password_ver
    from actions_with_password_obs import __version__ as actions_with_password_ver
    from datetime_obs import __version__ as datetime_ver
    from del_object_obs import __version__ as del_resource_ver
    from enc_obs import __version__ as enc_ver
    from get_size_obs import __version__ as get_size_ver
    from logo_obs import __version__ as logo_ver
    from notes_obs import __version__ as notes_ver
    from update_obs import __version__ as update_ver
    from show_dec_data_obs import __version__ as show_dec_ver
    from decryption_block_obs import __version__ as dec_block_ver

    system_action("clear")
    template_some_message(GREEN, '  - Versions installed modules -')

    def template_version_module(module, version):
        print(version, '  ---  ', module)

    template_version_module('get_size_obs', __version__)
    template_version_module('change_password_obs', change_password_ver)
    template_version_module('actions_with_password_obs', actions_with_password_ver)
    template_version_module('datetime_obs', datetime_ver)
    template_version_module('del_object_obs', del_resource_ver)
    template_version_module('enc_obs', enc_ver)
    template_version_module('get_size_obs', get_size_ver)
    template_version_module('logo_obs', logo_ver)
    template_version_module('notes_obs', notes_ver)
    template_version_module('update_obs', update_ver)
    template_version_module('show_dec_data_obs', show_dec_ver)
    template_version_module('decryption_block_obs', dec_block_ver)
    template_version_module('main', elba_v)


def size_all():
    """ Получении информации о занимаемой памяти в ОЗУ """
    template_some_message(BLUE, " - Volume taken up by the program - ")
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
        if len(str(size)) == 5:
            size = str(size) + ' '
        elif len(str(size)) == 4:
            size = str(size) + '  '
        print("{0}  ---  {1}".format(size, file))

    # Получение размера пользовательских файлов
    size_notes = size_resources = 0
    for folder_with_resource in os.listdir(FOLDER_WITH_RESOURCES):
        for file in os.listdir(FOLDER_WITH_RESOURCES + folder_with_resource):
            size_resources += os.path.getsize(FOLDER_WITH_RESOURCES + folder_with_resource + '/' + file)
    size_user_data += size_resources
    for folder_with_note in os.listdir(FOLDER_WITH_NOTES):
        for file in os.listdir(FOLDER_WITH_NOTES + folder_with_note):
            size_notes += os.path.getsize(FOLDER_WITH_NOTES + folder_with_note + '/' + file)
    size_user_data += size_notes
    for file in os.listdir(FOLDER_WITH_DATA):
        size_user_data += os.path.getsize(FOLDER_WITH_DATA + file)

    size_logs = os.path.getsize(FILE_LOG)

    def to_another_unit_of_measurement(__size__):
        """ Округление и перевод в единицы измерения """
        if 2**20 <= __size__:
            __size__ = round((__size__ / (2**20)), 1)
            user_measure = 'MiB'
        elif 2**10 <= __size__ < 2**20:
            __size__ = round((__size__ / (2**10)), 1)
            user_measure = 'KiB'
        else:
            __size__ = round(__size__, 1)
            user_measure = 'B'
        return YELLOW + str(__size__) + ' ' + user_measure + DEFAULT_COLOR

    program_in_ram = memory_usage()
    program_in_ram = program_in_ram[0] * 2**20

    total_size = size_program + size_mod_cache + size_user_data + size_logs
    data_to_print = {
        'The program occupies RAM ': to_another_unit_of_measurement(program_in_ram),
        '\nThe log files took     ': to_another_unit_of_measurement(size_logs),
        'User files took          ': to_another_unit_of_measurement(size_user_data),
        'The notes took           ': to_another_unit_of_measurement(size_notes),
        'The resources took       ': to_another_unit_of_measurement(size_resources),
        'The program files took up': to_another_unit_of_measurement(size_program),
        'The program cache took up': to_another_unit_of_measurement(size_mod_cache),
        'The total program takes  ': to_another_unit_of_measurement(total_size)
    }
    print('\n')
    for text, space_used in data_to_print.items():
        print("{0}  ---  {1}".format(text, space_used))
