#!/usr/bin/env python3
from main import *
import os


__version__ = '1.1.0'


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
        if item.endswith(".csv") or item.endswith(".dat") or item.endswith(".log"):
            size_user_data += os.path.getsize(user_folder + item)

    size_program += size_mod_cache  # Вычисление всего веса
    size_logs = os.path.getsize(user_folder + '.file.log')

    def template_output(text, value, measure):
        """ Шаблон вывода информации """
        print(text, YELLOW, value, measure, DEFAULT_COLOR)

    if size_user_data > 2**10:
        size_user_data /= 2**10
        size_user_data = round(size_user_data, 2)
        user_measure = 'Килобайт'
    else:
        user_measure = 'Байт'

    total_data = size_program + size_user_data + os.path.getsize('get_size_obs.py') + size_logs
    template_output('Лог-файлы заняли', rounding(size_logs), 'Килобайт')
    template_output('Данные пользователя заняли', size_user_data, user_measure)
    template_output('Файлы программы заняли', rounding(size_program - size_mod_cache), 'Килобайт')
    template_output('Кэш модулей занял', rounding(size_mod_cache), 'Килобайт')
    template_output('Итого весь проект занимает', rounding(total_data), 'Килобайт в ПЗУ')
