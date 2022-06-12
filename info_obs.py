#!/usr/bin/env python3

"""
    Модуль получения информации о программе: версий модулей, веса файлов
"""

from main import *

import csv
import os
import sys
import socket
from uuid import getnode as get_mac
import platform

from memory_profiler import memory_usage
import getpass
import functions_obs


__version__ = '0.10-01'


class Information(object):

    """
        Отображение информации о машине, версий модулей, а также о занимаемой памяти в ОЗУ и ПЗУ.
    """

    @staticmethod
    def get_info():
        functions_obs.StylishLook().topper('INFORMATION')
        print("_" * get_size_of_terminal())
        template_some_message(GREEN, '- Information about machine -')

        name = getpass.getuser()  # Имя пользователя
        mac = get_mac()  # MAC адрес
        sys_info = platform.uname()  # Название операционной системы
        update_sys_info = (name, str(mac)) + sys_info
        list_names_sys_info = [
            'User name',
            'MAC address',
            'System',
            'Computer name',
            'Release',
            'Version release',
            'Machine',
        ]

        for i in range(len(update_sys_info)):
            print("{:16s} - {:s}".format(list_names_sys_info[i], update_sys_info[i]))
        print("_" * get_size_of_terminal())

        # template_some_message(GREEN, '- Versions installed modules -')
        print("_" * get_size_of_terminal())
        template_some_message(GREEN, "- Space occupied in ROM -")
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
            print("{:6s}  ---  {:s}".format(str(size), file))

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
                __size__ = round((__size__ / (2**20)), 2)
                user_measure = 'MiB'
            elif 2**10 <= __size__ < 2**20:
                __size__ = round((__size__ / (2**10)), 2)
                user_measure = 'KiB'
            else:
                __size__ = round(__size__, 2)
                user_measure = 'B'
            return ACCENT_1 + f"{__size__} {user_measure}" + ACCENT_4

        program_in_ram = memory_usage()
        program_in_ram = program_in_ram[0] * 2**20

        total_size = size_program + size_mod_cache + size_user_data + size_logs
        data_to_print = {
            'The program occupies RAM ': to_another_unit_of_measurement(program_in_ram),
            '\nThe log file took        ': to_another_unit_of_measurement(size_logs),
            'User files took          ': to_another_unit_of_measurement(size_user_data),
            'The notes took           ': to_another_unit_of_measurement(size_notes),
            'The resources took       ': to_another_unit_of_measurement(size_resources),
            'The program files took up': to_another_unit_of_measurement(size_program),
            'The program cache took up': to_another_unit_of_measurement(size_mod_cache),
            'The total program takes  ': to_another_unit_of_measurement(total_size)
        }
        print('\n')
        for text, space_used in data_to_print.items():
            print("{0}{1}{2}  ---  {3}{4}".format(ACCENT_1, text, ACCENT_4, ACCENT_1, space_used))
        print("_" * get_size_of_terminal())
