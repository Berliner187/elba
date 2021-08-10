#!/usr/bin/env python3

"""
    Password Manager For Linux (SFL)
    Elba - Password manager, keeper notes and encryption files and folders
    Resources and notes related to them are encrypted with a single password
    Copyright (C) 2021  by Berliner187

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
"""

import os
import sys
import datetime
import shutil
from time import sleep
from csv import DictReader, DictWriter


__version__ = 'v0.8.5.2'


def get_size_of_terminal():
    """ Получение ширины и длины терминала """
    cols, rows = shutil.get_terminal_size()
    return cols


def show_name_program():
    from logo_obs import wait_effect
    edit_version = __version__ + '       '
    lines = [BLUE,
             "||  Delta For Linux  ||",
             "||  by Berliner187   ||",
             "||  Veli Afaline     ||",
             YELLOW, edit_version
             ]
    wait_effect(lines, 0.0001)
    if CHECK_FOLDER_FOR_RESOURCE is False:
        first_start_message()


def system_action(action):
    """ Системные действия """
    if action == 'restart':
        os.execv(sys.executable, [sys.executable] + sys.argv)
    if action == 'clear':
        os.system('cls' if os.name == 'nt' else 'clear')
    if action == 'file_manager':
        os.system('explorer.exe .' if os.name == 'nt' else 'nautilus .')
    else:
        os.system(action)


def template_remove_folder(some_folder):
    """ Шаблон удаления папки """
    os.system('rmdir ' + some_folder if os.name == 'nt' else 'rm -r ' + some_folder + ' -f')


def template_some_message(color, message):
    """ Шаблон сообщения в ходе работы программы """
    cols, rows = shutil.get_terminal_size()
    print(color, '\n'*2, message.center(cols), DEFAULT_COLOR)


def template_for_install(program_file):
    """ Шаблон установки файлов программы """
    os.system(get_peculiarities_copy('move') + FOLDER_ELBA + program_file + ' . ')


def template_question(text):
    """ Шаблон вопросов от программы """
    question = input(YELLOW + f" - {text} (y/n): " + DEFAULT_COLOR)
    return question


# <<<----------------------- Константы --------------------------->>>
# Папки
FOLDER_ELBA = 'elba/'
FOLDER_WITH_DATA = 'volare/'  # Mi fa volare
FOLDER_WITH_PROGRAM_DATA = FOLDER_WITH_DATA + 'program_files/'
FOLDER_WITH_RESOURCES = FOLDER_WITH_DATA + 'resources/'
FOLDER_WITH_NOTES = FOLDER_WITH_DATA + 'notes/'
OLD_ELBA = 'old_elba/'
# <<<----------- Имена файлов и папок для шифрования ------------>>>
FOLDER_WITH_ENC_DATA = FOLDER_WITH_DATA + 'ENCRYPTION_DATA/'
FOLDER_FOR_ENCRYPTION_FILES = FOLDER_WITH_ENC_DATA + 'FOR_ENCRYPTION'
PREFIX_FOR_DEC_FILE = 'DEC_'
FILE_CONTROL_SUM = 'CONTROL.dat'
KEY_FILE = 'BESTE.key'
IV_FILE = 'LEBEN.key'
SIGNED = 'SIGN.dat'
# <<<------------ Имена файлов для ресурсов и заметок ------------>>>
FILE_RESOURCE = 'resource.dat'
FILE_LOGIN = 'login.dat'
FILE_PASSWORD = 'password.dat'
FILE_NOTE_NAME = 'name_note.dat'
FILE_NOTE_ITSELF = 'note_itself.dat'
# <<<----------------------- Имена файлов программы ------------------------>>>
FILE_WITH_HASH_GENERIC_KEY = FOLDER_WITH_PROGRAM_DATA + '.hash_generic_key.dat'
FILE_WITH_GENERIC_KEY = FOLDER_WITH_PROGRAM_DATA + '.generic_key.dat'
FILE_USER_NAME = FOLDER_WITH_PROGRAM_DATA + '.self_name.dat'
FILE_WITH_HASH = FOLDER_WITH_PROGRAM_DATA + '.hash_password.dat'
FILE_LOG = FOLDER_WITH_PROGRAM_DATA + '.file.log'
FILE_SETTINGS_COLOR = FOLDER_WITH_PROGRAM_DATA + 'setting_color_accent.ini'
# <<<------------- Проверка файлов на наличие --------------->>>
CHECK_FILE_WITH_GENERIC = os.path.exists(FILE_WITH_HASH_GENERIC_KEY)
CHECK_FILE_WITH_HASH = os.path.exists(FILE_WITH_HASH)
CHECK_FOLDER_FOR_RESOURCE = os.path.exists(FOLDER_WITH_RESOURCES)
# <<<----------- Столбцы файла с логами ------------->>>
FIELDS_LOG_FILE = ['version', 'date', 'cause', 'status']

# <<<--------------  Репозиторий для обновлений  -------------->>>
REPOSITORY = 'git clone https://github.com/Berliner187/elba -b delta'

# <<<--------------  Модули для работы программы  -------------->>>
stock_modules = [
    'datetime_obs.py', 'enc_obs.py', 'logo_obs.py', 'del_object_obs.py',
    'notes_obs.py', 'get_size_obs.py', 'change_password_obs.py',
    'actions_with_password_obs.py', 'show_dec_data_obs.py',
    'decryption_block_obs.py'
]

# Цвета акцента цветов по умолчанию
dictionary_colors = {
    'ACCENT_1': '#FBC330',
    'ACCENT_2': '#9B30FF',
    'ACCENT_3': '#30A0E0',
    'ACCENT_4': '#2ECC71',
    'ACCENT_5': '#C70039',
    'ACCENT_6': '#FFFFFF'
}
if os.path.exists(FILE_SETTINGS_COLOR) is False:
    # Сохранение цветов в файл
    with open(FILE_SETTINGS_COLOR, 'w+') as f:
        f.write(str(dictionary_colors))
else:
    # Получение акцента цветов из файла
    dic_colors = ''
    with open(FILE_SETTINGS_COLOR, 'r') as file_accent:
        for i in file_accent.readlines():
            dic_colors = i
    dictionary_colors = eval(dic_colors)
# Ключи словаря с цветами добавляются в массив
massive_colors = []
for accent in dictionary_colors:
    massive_colors.append(accent)


def format_hex_color(hex_color):
    """ Получение цвета в формате HEX """
    r, g, b = [int(hex_color[item:item+2], 16) for item in range(1, len(hex_color), 2)]
    return f"\x1b[38;2;{r};{g};{b}m".format(**vars())


# Цвета в терминале
YELLOW = format_hex_color(dictionary_colors[massive_colors[0]])
PURPLE = format_hex_color(dictionary_colors[massive_colors[1]])
BLUE = format_hex_color(dictionary_colors[massive_colors[2]])
GREEN = format_hex_color(dictionary_colors[massive_colors[3]])
RED = format_hex_color(dictionary_colors[massive_colors[4]])
DEFAULT_COLOR = format_hex_color(dictionary_colors[massive_colors[5]])

# Создание основных папок
FOLDERS = [FOLDER_WITH_DATA, FOLDER_WITH_NOTES, FOLDER_WITH_PROGRAM_DATA]
for folder in FOLDERS:
    if os.path.exists(folder) is False:
        os.mkdir(folder)


def get_peculiarities_copy(type_copy):
    """ Поддержка синтаксиса командных оболочек Linux, MacOS X и Windows """
    if type_copy == 'dir':
        if os.name == 'nt':
            peculiarities_copy = 'xcopy /y /o /e '
        else:
            peculiarities_copy = 'cp -r '
        return peculiarities_copy
    elif type_copy == 'file':
        if os.name == 'nt':
            peculiarities_copy = 'copy '
        else:
            peculiarities_copy = 'cp '
        return peculiarities_copy
    elif type_copy == 'move':
        if os.name == 'nt':
            peculiarities_move = 'move '
        else:
            peculiarities_move = 'mv '
        return peculiarities_move


def download_from_repository():
    """ Загрузка и установка из репозитория модуля обновлений """
    os.system(REPOSITORY)
    system_action('clear')
    if os.path.exists('update_obs.py') is False:
        os.system(get_peculiarities_copy('move') + ' elba/update_obs.py .')
        system_action('restart')


def write_log(cause, status_itself):
    """ Логирование """
    def get_time_now():      # Получение и форматирование текущего времени
        hms = datetime.datetime.today()
        time_format = f"{hms.hour}:{hms.minute}:{hms.second}"
        date_format = f"{hms.day}.{hms.month}.{hms.year}"
        total = f"{time_format}-{date_format}"
        return ''.join(total)

    if os.path.exists(FILE_LOG) is False:
        with open(FILE_LOG, mode="a", encoding='utf-8') as data:
            logs_writer = DictWriter(data, fieldnames=FIELDS_LOG_FILE, delimiter=';')
            logs_writer.writeheader()

    log_data = open(FILE_LOG, mode="a", encoding='utf-8')
    log_writer = DictWriter(log_data, fieldnames=FIELDS_LOG_FILE, delimiter=';')
    log_writer.writerow({
        FIELDS_LOG_FILE[0]: __version__,     # Запись версии
        FIELDS_LOG_FILE[1]: get_time_now(),  # Запись даты и времени
        FIELDS_LOG_FILE[2]: cause,           # Запись причины
        FIELDS_LOG_FILE[3]: status_itself    # Запись статуса
    })


def check_modules():
    """ Проверка модулей программы """
    cnt_missing_modules = 0
    file_type = 'obs.py'
    installed_modules = []
    for file in os.listdir('.'):
        if file.endswith(file_type):
            installed_modules.append(file)
    for i in range(len(stock_modules)):
        if stock_modules[i] not in installed_modules:
            cnt_missing_modules += 1
    if cnt_missing_modules > 0:
        template_some_message(RED, " - Missing module/modules -")
        write_log('Missing module/modules', 'FAIL')
        return 1
    else:
        return 0


def launcher():
    """ The main function responsible for the operation of the program """
    system_action('clear')
    if CHECK_FOLDER_FOR_RESOURCE is False:  # При первом запуске
        show_name_program()
        elba()
        master_password = ActionsWithPassword('master').get_password()
        generic_key = ActionsWithPassword('generic').get_password()
        greeting(generic_key)
        enc_aes(FILE_WITH_GENERIC_KEY, generic_key, master_password)
        os.mkdir(FOLDER_WITH_RESOURCES)
        show_decryption_data(generic_key, 'resource')
        write_log('First launch', 'OK')
        decryption_block(generic_key)
    else:  # При последующем
        master_password = point_of_entry()
        generic_key_from_file = dec_aes(FILE_WITH_GENERIC_KEY, master_password)
        system_action('clear')
        greeting(generic_key_from_file)
        write_log('Subsequent launch', 'OK')
        show_decryption_data(generic_key_from_file, 'resource')
        decryption_block(generic_key_from_file)


if __name__ == '__main__':
    system_action('clear')
    try:
        from update_obs import update, install_old_saved_version
    except ModuleNotFoundError as update_obs_error:
        write_log(update_obs_error, 'FAILED')
        template_some_message(RED, ' - Module "update" does not exist - ')
        download_from_repository()

    try:
        from werkzeug.security import generate_password_hash, check_password_hash
        from stdiomask import getpass
        import Crypto.Hash
        import memory_profiler
    except ModuleNotFoundError as error_module:
        write_log(error_module, 'CRASH')
        template_some_message(RED, f"MISSING: {error_module}")
        template_some_message(
            YELLOW, f"Please, install{str(error_module)[15:]} with requirements"
        )
        quit()

    status_mis_mod = check_modules()
    if status_mis_mod == 0:
        from decryption_block_obs import decryption_block
        from actions_with_password_obs import point_of_entry
        from enc_obs import enc_aes, dec_aes
        from datetime_obs import greeting
        from show_dec_data_obs import show_decryption_data
        from actions_with_password_obs import ActionsWithPassword
        from logo_obs import first_start_message, elba

        try:
            launcher()  # Запуск лончера
        except Exception as random_error:
            write_log(random_error, 'FAIL')
            template_some_message(RED, ' --- ERROR --- ')
            print(random_error)
            sleep(1)
            system_action('clear')
            print(BLUE,
                  '\n - Enter 1 to update \n'
                  ' - Enter 2 to rollback ')
            rollback_or_update = input(YELLOW + '\n - Select by number: ' + DEFAULT_COLOR)
            if rollback_or_update == '1':  # Попытка откатиться
                template_some_message(RED, '-- You can try roll back --')
                change = input(template_question(' - Roll back? (y/n): '))
                if change == 'y':
                    install_old_saved_version()
            elif rollback_or_update == '2':  # Попытка обновиться
                get_confirm = input(template_question(" - Update? (y/n): "))
                if get_confirm == 'y':
                    write_log('Try update', 'Run')
                    update()
                else:
                    write_log('Exit', 'OK')
                    quit()
            else:
                system_action('clear')
                template_some_message(RED, ' - Error in change - ')
                sleep(1)
            system_action('restart')
        except KeyError:
            pass
    else:
        update()
