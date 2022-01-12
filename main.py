#!/usr/bin/env python3

"""
    Password Manager For Linux (SFL)
    Elba - Password manager, keeper notes and encryption files and folders
    Resources and notes related to them are encrypted with a single password
    Copyright (C) 2022  by Berliner187

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


__version__ = '0.9.0.6'


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
KEY_FILE = '___KEY_1___.key'
IV_FILE = '___KEY_2___.key'
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
FILE_PROGRAM_INFO = FOLDER_WITH_PROGRAM_DATA + 'info.dat'
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
    'datetime_obs.py', 'enc_obs.py', 'logo_obs.py',
    'del_object_obs.py', 'notes_obs.py', 'information_obs.py',
    'actions_with_password_obs.py', 'category_actions_obs.py',
    'decryption_block_obs.py', 'settings_obs.py', 'update_obs.py'
]

# <<< -------- Цветовые акценты в программе -------- >>>
dictionary_colors = {
    'ACCENT_1': '#FBC330',
    'ACCENT_2': '#9B30FF',
    'ACCENT_3': '#30A0E0',
    'ACCENT_4': '#FFFFFF',
}

# <<< ------- ШИРОКО ИСПОЛЬЗУЕМЫЕ ФУНКЦИИ ------- >>>


def get_size_of_terminal():
    """ Получение ширины и длины терминала """
    cols, rows = shutil.get_terminal_size()
    return cols


def show_name_program():
    from logo_obs import wait_effect
    edit_version = __version__ + ' '
    lines = [ACCENT_3,
             "||  Delta For Linux  ||",
             "||  by Berliner187   ||",
             "||  Seal Barrilla    ||",
             ACCENT_1, edit_version
             ]
    wait_effect(lines, 0.0001)
    if CHECK_FOLDER_FOR_RESOURCE is False:
        first_start_message()


def template_remove_folder(some_folder):
    """ Шаблон удаления папки """
    os.system('rmdir ' + some_folder if os.name == 'nt' else 'rm -r ' + some_folder + ' -f')


def template_some_message(color, message):
    """ Шаблон сообщения в ходе работы программы """
    cols = get_size_of_terminal()
    print(color, '\n'*2, f"{message.center(cols)}{ACCENT_4}")


def template_for_install(program_file):
    """ Шаблон установки файлов программы """
    os.system(get_peculiarities_system('move') + FOLDER_ELBA + program_file + ' . ')


def template_question(text):
    """ Шаблон вопросов от программы """
    return input(ACCENT_1 + f" - {text} (y/n): " + ACCENT_4)


def template_input(text):
    return input(ACCENT_1 + f" - {text} " + ACCENT_4)


def format_hex_color(hex_color):
    """ Получение цвета в формате HEX """
    r, g, b = [int(hex_color[item:item+2], 16) for item in range(1, len(hex_color), 2)]
    return f"\x1b[38;2;{r};{g};{b}m".format(**vars())


# Создание основных папок
FOLDERS = [
    FOLDER_WITH_DATA, FOLDER_WITH_NOTES,
    FOLDER_WITH_PROGRAM_DATA, FOLDER_WITH_ENC_DATA
]
for folder in FOLDERS:
    if os.path.exists(folder) is False:
        os.mkdir(folder)


# <<< ----------- ЦВЕТОВЫЕ АКЦЕНТЫ ------------- >>>
# Работа с акцентами в файле
if os.path.exists(FILE_SETTINGS_COLOR) is False:
    with open(FILE_SETTINGS_COLOR, 'w') as f:
        f.write('')
        f.close()
    # Сохранение цветов в файл
    with open(FILE_SETTINGS_COLOR, 'w+') as f:
        f.write(str(dictionary_colors))
else:
    # Получение акцента цветов из файла
    dic_colors = ''
    with open(FILE_SETTINGS_COLOR, 'r') as file_accent:
        for i in file_accent.readlines():
            dic_colors = i
        file_accent.close()
    dictionary_colors = eval(dic_colors)
# Ключи словаря с цветами добавляются в массив
massive_colors = []
for accent in dictionary_colors:
    massive_colors.append(accent)
# Цвета в терминале
ACCENT_1 = format_hex_color(dictionary_colors[massive_colors[0]])
ACCENT_2 = format_hex_color(dictionary_colors[massive_colors[1]])
ACCENT_3 = format_hex_color(dictionary_colors[massive_colors[2]])
ACCENT_4 = format_hex_color(dictionary_colors[massive_colors[3]])
GREEN = format_hex_color('#2ECC71')
RED = format_hex_color('#C70039')


# <<< ------- ДЕЙСТВИЯ С СИСТЕМОЙ ------- >>>
def system_action(action):
    """ Системные действия (выполнение действия) """
    if action == 'restart':
        system_action('clear')
        template_some_message(GREEN, '--- Restart ---')
        sleep(.2)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    if action == 'clear':
        # print('\n'*3)
        os.system('cls' if os.name == 'nt' else 'clear')
    if action == 'file_manager':
        if os.name == 'nt':
            os.system('explorer.exe .')
    else:
        if action != 'clear':
            os.system(action)


def get_peculiarities_system(action):
    """
        Поддержка синтаксиса командных оболочек Linux, MacOS X и Windows
        (возвращение аргументов к действиям)
    """
    if action == 'copy_dir':
        if os.name == 'nt':
            peculiarities_system_action = 'xcopy /y /o /e '
        else:
            peculiarities_system_action = 'cp -r '
    elif action == 'rm_dir':
        if os.name == 'nt':
            peculiarities_system_action = 'rmdir '
        else:
            peculiarities_system_action = 'rm -r '
    elif action == 'mkdir':
        if os.name == 'nt':
            peculiarities_system_action = 'makedir '
        else:
            peculiarities_system_action = 'mkdir '
    elif action == 'file':
        if os.name == 'nt':
            peculiarities_system_action = 'copy '
        else:
            peculiarities_system_action = 'cp '
    elif action == 'move':
        if os.name == 'nt':
            peculiarities_system_action = 'move '
        else:
            peculiarities_system_action = 'mv '
    elif action == 'rm':
        if os.name == 'nt':
            peculiarities_system_action = 'del '
        else:
            peculiarities_system_action = 'rm '
    else:
        peculiarities_system_action = "echo No action selected"
    return peculiarities_system_action


def download_from_repository():
    """ Загрузка и установка из репозитория модуля обновлений """
    os.system(REPOSITORY)
    module_update = 'update_obs.py'
    system_action('clear')
    if os.path.exists(module_update) is False:
        os.system(get_peculiarities_system('move') + f' elba/{module_update} .')
        system_action('restart')


def write_log(cause, status_itself):
    """ Логирование """
    def get_time_now():      # Получение и форматирование текущего времени
        hms = datetime.datetime.today()
        time_format = f"{hms.hour}:{hms.minute}:{hms.second}"
        date_format = f"{hms.day}.{hms.month}.{hms.year}"
        return f"{time_format}-{date_format}"

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
    log_data.close()


def check_modules():
    """ Проверка модулей программы """
    cnt_missing_modules = 0
    file_type = 'obs.py'
    installed_modules = []
    for file in os.listdir('.'):
        if file.endswith(file_type):
            installed_modules.append(file)
    for mod in range(len(stock_modules)):
        if stock_modules[mod] not in installed_modules:
            cnt_missing_modules += 1
    if cnt_missing_modules == 0:
        return 0
    else:
        template_some_message(RED, "- Missing module(-s) -")
        write_log('Missing module(-s)', 'FAIL')
        return 1


def launcher():
    """ The main function responsible for the operation of the program """
    system_action('clear')
    write_log('-', '-')
    Information().save_modules_info()
    if CHECK_FOLDER_FOR_RESOURCE is False:  # При первом запуске
        show_name_program()
        master_password = ActionsWithPassword('master').get_password()
        generic_key = ActionsWithPassword('generic').get_password()
        greeting(generic_key)
        enc_aes(FILE_WITH_GENERIC_KEY, generic_key, master_password)
        os.mkdir(FOLDER_WITH_RESOURCES)
        CategoryActions(generic_key, 'resource').get_category_label()
        write_log('First launch', 'OK')
        decryption_block(generic_key)
    else:  # При последующем
        master_password = ActionsWithPassword(None).point_of_entry()
        generic_key_from_file = dec_aes(FILE_WITH_GENERIC_KEY, master_password)
        system_action('clear')
        greeting(generic_key_from_file)
        write_log('Authorization', 'OK')
        CategoryActions(generic_key_from_file, 'resource').get_category_label()
        decryption_block(generic_key_from_file)


if __name__ == '__main__':
    system_action('clear')
    try:
        from update_obs import update, install_old_saved_version
    except ModuleNotFoundError as update_obs_error:
        write_log(update_obs_error, 'FAILED')
        template_some_message(RED, '- Module "update" does not exist -')
        download_from_repository()

    try:
        from werkzeug.security import generate_password_hash, check_password_hash
        from stdiomask import getpass
    except ModuleNotFoundError as error_module:
        write_log(error_module, 'CRASH')
        template_some_message(RED, f"MISSING: {error_module}")
        template_some_message(
            ACCENT_1, f"Please, install {str(error_module)[15:]} with requirements"
        )
        quit()

    # Проверка модулей на наличие
    status_mis_mod = check_modules()
    # Если модули на месте
    if status_mis_mod == 0:
        from decryption_block_obs import decryption_block
        from enc_obs import enc_aes, dec_aes
        from datetime_obs import greeting
        from category_actions_obs import CategoryActions
        from actions_with_password_obs import ActionsWithPassword
        from logo_obs import first_start_message, elba
        from information_obs import Information

        try:
            launcher()  # Запуск лончера
        except Exception or NameError as random_error:
            write_log(random_error, 'FAIL')
            template_some_message(RED, ' --- ERROR --- ')
            print(random_error)
            sleep(1)
            system_action('clear')
            print(f"{ACCENT_3}"
                  f'\n - Enter 1 to rollback'
                  f'\n - Enter 2 to update')
            rollback_or_update = input(ACCENT_1 + '\n - Select by number: ' + ACCENT_4)

            if rollback_or_update == '1':  # Попытка откатиться
                template_some_message(RED, '-- You can try roll back --')
                change = input(template_question(' - Roll back? (y/n): '))
                if change == 'y':
                    install_old_saved_version()
            elif rollback_or_update == '2':  # Попытка обновиться
                get_confirm = input(template_question(" - Update? (y/n): "))
                if get_confirm == 'n':
                    write_log('Exit', 'OK')
                    quit()
                else:
                    write_log('Try update', 'Run')
                    update()
            else:
                system_action('clear')
                template_some_message(RED, '- Error in change -')
                sleep(1)
            system_action('restart')

        except KeyError:
            pass
        except KeyboardInterrupt as keyboard:
            system_action('clear')
            template_some_message(ACCENT_3, '--- ELBA CLOSED ---')
            write_log(keyboard, "CLOSE")
            quit()
    else:
        update()
