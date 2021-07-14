#!/usr/bin/env python3

"""
    Password Manager For Linux (SFL)
    Elba - Password manager and keeper notes
    Resources and notes related to them are encrypted with a single password
    Copyright (C) 2021  by Berliner187

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
"""

import os
import sys
from time import sleep
from csv import DictReader, DictWriter
import datetime


__version__ = 'v0.7.0.2'


def show_name_program():
    print(BLUE,
          "\n || Password Manager and Keeper of Notes ||",
          "\n || Delta For Linux || "
          "\n || by Berliner187  || ", YELLOW,
          "\n\n ||  Henette Zuer   || ", BLUE, __version__)
    if CHECK_FOLDER_FOR_RESOURCE is False:
        first_start_message()


def system_action(action):
    """ Restart Program or Clear terminal """
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
    print(color, '\n\n', message, DEFAULT_COLOR)


# Цвета в терминале
YELLOW, BLUE, PURPLE = "\033[33m", "\033[36m", "\033[35m"
GREEN, RED, DEFAULT_COLOR = "\033[32m", "\033[31m", "\033[0m"

# <<<-------------------- Константы ------------------------->>>
# Папки
FOLDER_ELBA = 'elba/'
FOLDER_WITH_DATA = 'volare/'  # Mi fa volare
FOLDER_WITH_PROGRAM_DATA = FOLDER_WITH_DATA + 'program_files/'
FOLDER_WITH_RESOURCES = FOLDER_WITH_DATA + "resources/"
FOLDER_WITH_NOTES = FOLDER_WITH_DATA + 'notes/'
OLD_ELBA = 'old_elba/'
# <<<-------- Имена файлов и папок для шифрования --------->>>
FOLDER_WITH_ENC_DATA = FOLDER_WITH_DATA + 'ENCRYPTION_DATA/'
FOLDER_FOR_ENCRYPTION_FILES = FOLDER_WITH_ENC_DATA + 'FOR_ENCRYPTION'
PREFIX_FOR_DEC_FILE = '_DEC'
# Получение времени
hms = datetime.datetime.today()
get_date = str(hms.day) + str(hms.month) + str(hms.year) + '_'
get_time = str(hms.hour * 3600 + hms.minute * 60 + hms.second)
NAME_ENC_FOLDER = get_date + get_time
FOLDER_WITH_ENC_FILES = FOLDER_WITH_ENC_DATA + NAME_ENC_FOLDER
KEY_FILE = 'ONE.key'
IV_FILE = 'TWO.key'
# <<<--- Имена файлов для ресурсов и заметок --->>>
FILE_RESOURCE = 'resource.dat'
FILE_LOGIN = 'login.dat'
FILE_PASSWORD = 'password.dat'
FILE_NOTE_NAME = 'name_note.dat'
FILE_NOTE_ITSELF = 'note_itself.dat'
# <<<----------------------- Имена файлов программы ------------------------>>>
FILE_WITH_HASH_GENERIC_KEY = FOLDER_WITH_PROGRAM_DATA + '.hash_generic_key.dat'
FILE_WITH_GENERIC_KEY = FOLDER_WITH_PROGRAM_DATA + '.generic_key.dat'
FILE_USER_NAME = FOLDER_WITH_PROGRAM_DATA + ".self_name.dat"
FILE_WITH_HASH = FOLDER_WITH_PROGRAM_DATA + '.hash_password.dat'
FILE_LOG = FOLDER_WITH_PROGRAM_DATA + '.file.log'
# <<<------------- Проверка файлов на наличие --------------->>>
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

FOLDERS = [FOLDER_WITH_DATA, FOLDER_WITH_NOTES, FOLDER_WITH_PROGRAM_DATA]
for folder in FOLDERS:
    if os.path.exists(folder) is False:
        os.mkdir(folder)


def download_from_repository():
    """ Загрузка и установка из репозитория модуля обновлений """
    os.system(REPOSITORY)
    system_action('clear')
    if os.path.exists('update_obs.py') is False:
        os.system('mv elba/update_obs.py .')
        system_action('restart')


def write_log(cause, status_itself):
    """ Логирование """
    def get_time_now():      # Получение и форматирование текущего времени
        time_format = str(hms.hour) + ':' + str(hms.minute) + ':' + str(hms.second)
        date_format = str(hms.day) + '.' + str(hms.month) + '.' + str(hms.year)
        total = str(time_format) + '-' + str(date_format)
        return ''.join(total)

    log_data = open(FILE_LOG, mode="a", encoding='utf-8')
    log_writer = DictWriter(log_data, fieldnames=FIELDS_LOG_FILE, delimiter=';')
    if os.path.exists(FILE_LOG) is False:
        logs_writer.writeheader()
    log_writer.writerow({
        FIELDS_LOG_FILE[0]: __version__,     # Запись версии
        FIELDS_LOG_FILE[1]: get_time_now(),      # Запись даты и времени
        FIELDS_LOG_FILE[2]: cause,           # Запись причины
        FIELDS_LOG_FILE[3]: status_itself    # Запись статуса
    })


def launcher():
    """ The main function responsible for the operation of the program """
    if os.path.exists(FILE_LOG) is False:
        with open(FILE_LOG, mode="a", encoding='utf-8') as data:
            logs_writer = DictWriter(data, fieldnames=FIELDS_LOG_FILE, delimiter=';')
            logs_writer.writeheader()

    if CHECK_FOLDER_FOR_RESOURCE is False:  # При первом запуске
        show_name_program()
        elba()
        master_password = ActionsWithPassword('master').get_password()  # Создание мастер-пароля
        genetic_key = ActionsWithPassword('generic').get_password()  # Генерирование generic-key
        greeting(genetic_key)
        os.mkdir(FOLDER_WITH_RESOURCES)
        decryption_block(genetic_key)
        enc_aes(FILE_WITH_GENERIC_KEY, genetic_key, master_password)
        write_log('First launch', 'OK')
        system_action('restart')
    else:  # При последующем
        master_password = point_of_entry()
        genetic_key_from_file = dec_aes(FILE_WITH_GENERIC_KEY, master_password)
        system_action('clear')
        greeting(genetic_key_from_file)
        system_action('clear')
        write_log('Subsequent launch', 'OK')
        show_decryption_data(genetic_key_from_file, 'resource')
        decryption_block(genetic_key_from_file)


def check_modules():
    """ Проверка модулей программы """
    cnt_missing_modules = 0
    file_type = 'obs.py'
    any_file = os.listdir('.')
    installed_modules = []
    for file in any_file:
        if file.endswith(file_type):
            installed_modules.append(file)
    for i in range(len(stock_modules)):
        if stock_modules[i] not in installed_modules:
            cnt_missing_modules += 1
    if cnt_missing_modules > 0:
        template_some_message(RED, " - Missing module/modules -")
        return 1
    else:
        return 0


if __name__ == '__main__':
    system_action('clear')
    try:
        from update_obs import update, install_old_saved_version
        try:
            from werkzeug.security import generate_password_hash, check_password_hash
            from stdiomask import getpass
        except ModuleNotFoundError as error_module:
            write_log(error_module, 'CRASH')
            print(RED, 'Error: \n' + str(error_module), DEFAULT_COLOR)
            print('\n')
            template_some_message(
                YELLOW, "Please, install module/modules with requirements"
            )
            quit()
    except ModuleNotFoundError as update_obs_error:
        write_log(update_obs_error, 'FAILED')
        template_some_message(RED, ' - Module "update" does not exist - ')
        sleep(1)
        download_from_repository()

    status = check_modules()
    if status == 0:
        from decryption_block_obs import decryption_block
        from actions_with_password_obs import point_of_entry
        from enc_obs import enc_aes, dec_aes
        from datetime_obs import greeting
        from show_dec_data_obs import show_decryption_data
        from actions_with_password_obs import ActionsWithPassword
        from logo_obs import first_start_message, elba

        try:
            launcher()  # Запуск лончера
        except ValueError or TypeError as error:
            print(error)
            write_log(error, 'CRITICAL CRASH')
            template_some_message(RED, ' --- Critical error, program is restarted --- ')
            sleep(1)
            system_action('clear')
            # Попытка откатиться, если возникает ошибка
            if os.path.exists(OLD_ELBA):
                template_some_message(RED, ' -- You can try roll back -- \n')
                change = input(YELLOW + ' - Roll back? (y/n): ' + DEFAULT_COLOR)
                if change == 'y':
                    install_old_saved_version()
            else:
                # Попытка обновиться, если возникает ошибка
                update()
            system_action('restart')
    else:
        update()
