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
import time
from time import sleep
from csv import DictReader, DictWriter


__version__ = '0.10.7_ALPHA'


# <<<----------------------- Константы --------------------------->>>
# <--- Директории --->
FOLDER_ELBA = 'elba/'
FOLDER_WITH_DATA = 'seele/'  # Zwei Seelen
FOLDER_WITH_PROGRAM_DATA = FOLDER_WITH_DATA + 'Program_Files/'
FOLDER_WITH_RESOURCES = FOLDER_WITH_DATA + 'RESOURCES/'
FOLDER_WITH_NOTES = FOLDER_WITH_DATA + 'NOTES/'
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
FILE_LOG = FOLDER_WITH_PROGRAM_DATA + 'elba.log'
FILE_SETTINGS_THEMES = FOLDER_WITH_PROGRAM_DATA + 'settings_themes.ini'
FILE_SETTINGS_COLOR = FOLDER_WITH_PROGRAM_DATA + 'setting_color_accent.ini'
FILE_PROGRAM_INFO = FOLDER_WITH_PROGRAM_DATA + 'info.dat'
FILE_WITH_SHA256 = 'ELBA_CPA.sign'  # Confirmed Protocol Authenticity
FILE_TOKEN = FOLDER_WITH_PROGRAM_DATA + 'token.dat'
FILE_FACTORY_UNLOCK_KEY = FOLDER_WITH_PROGRAM_DATA + '.unlock.key'
# FILE_WITH_SECRET_KEY_FOR_SHA256 = ''
# <<<------------- Проверка файлов на наличие --------------->>>
CHECK_FILE_WITH_GENERIC = os.path.exists(FILE_WITH_HASH_GENERIC_KEY)
CHECK_FILE_WITH_HASH = os.path.exists(FILE_WITH_HASH)
CHECK_FOLDER_FOR_RESOURCE = os.path.exists(FOLDER_WITH_RESOURCES)

# <<<----------- Столбцы файла с логами ------------->>>
FIELDS_LOG_FILE = ['version', 'date', 'status', 'cause']
# <<<--------------  Репозиторий для обновлений  -------------->>>
REPOSITORY = 'git clone https://github.com/Berliner187/elba -b delta'
# <<<--------------  Модули для работы программы  -------------->>>
stock_modules = [
    'change_mp_obs.py', 'control_bus_obs.py', 'datetime_obs.py',
    'functions_obs.py', 'getpass_obs.py', 'info_obs.py',
    'logo_obs.py', 'notes_obs.py', 'passwords_obs.py',
    'remove_obs.py', 'resources_obs.py', 'rollback_obs.py',
    'security_obs.py', 'settings_obs.py'
]
# <<< -------- Цветовые акценты в программе -------- >>>
dictionary_default_accents = {
    'ACCENT_1': '#EAE7E3',
    'ACCENT_2': '#BDB4AA',
    'ACCENT_3': '#9C9792',
    'ACCENT_4': '#FFFFFF',
    'ACCENT_5': '#5FC599'
}


# <<< ------- ШИРОКО ИСПОЛЬЗУЕМЫЕ ФУНКЦИИ ------- >>>
def get_size_of_terminal():
    """ Получение ширины и длины терминала """
    cols, rows = shutil.get_terminal_size()
    return cols


def show_name_program():
    from logo_obs import wait_effect, first_start_message
    if os.path.exists(FOLDER_WITH_RESOURCES) is False:
        first_start_message()
    lines = [
        ACCENT_2,
        f"E  DELTA FOR UNIX  A",
        f"L    Mino Arimo    B",
        f"B   {__version__}   L",
        f"A  by Berliner187  E",
        ACCENT_3,
        "_" * get_size_of_terminal()
    ]
    wait_effect(lines, 0)


def standard_location(right_now):
    return f"\n ELBA{right_now} ~E "
    # return input(ACCENT_1 + f"\n ELBA{right_now}: ~$ " + ACCENT_4)


def template_some_message(color, message):
    """ Шаблон сообщения в ходе работы программы """
    print(color, '\n\n', f"{message.center(get_size_of_terminal())}{ACCENT_4}")


def template_question(text):
    """ Шаблон вопросов от программы """
    return input(ACCENT_1 + f" - {text} (y/n): " + ACCENT_4)


def template_input(text):
    return input(ACCENT_1 + f"\n {text} " + ACCENT_4)


def template_warning_message(color, text):
    print(color)
    print(('=' * len(text)).center(get_size_of_terminal()))
    print(text.center(get_size_of_terminal()))
    print(('=' * len(text)).center(get_size_of_terminal()), ACCENT_4)


def template_print_decryption_data(data_type, path, generic_key):
    """ Шаблон отображения названий сервисов/заметок """
    from security_obs import dec_aes
    print(" {:8s} {:s}---{:s} {:s}".format(
        data_type, ACCENT_2, ACCENT_4,
        dec_aes(path, generic_key)))


def template_for_install(program_file):
    # setup template
    """ Шаблон установки файлов программы """
    os.system(get_peculiarities_system('copy_file') + FOLDER_ELBA + program_file + ' . ')


def template_remove_folder(some_folder):
    """ Шаблон удаления папки """
    os.system('rmdir ' + some_folder if os.name == 'nt' else 'rm -r ' + some_folder + ' -f')


def format_hex_color(hex_color):
    """ Получение цвета в формате HEX """
    r, g, b = [int(hex_color[item:item+2], 16) for item in range(1, len(hex_color), 2)]
    return f"\x1b[38;2;{r};{g};{b}m".format(**vars())


# Создание основных директорий
FOLDERS = [
    FOLDER_WITH_DATA, FOLDER_WITH_NOTES,
    FOLDER_WITH_PROGRAM_DATA, FOLDER_WITH_ENC_DATA
]
for folder in FOLDERS:
    if os.path.exists(folder) is False:
        os.mkdir(folder)


# <<< ----------- ЦВЕТОВЫЕ АКЦЕНТЫ ------------- >>>
def create_file_with_theme(record_content):
    # Сохранение цветов в файл
    with open(FILE_SETTINGS_COLOR, 'w+') as f:
        f.write('')
        f.write(str(record_content))
        f.close()


# < ----- Работа с акцентами в файле >
if os.path.exists(FILE_SETTINGS_COLOR) is False:    # При отсутствии файла
    create_file_with_theme(dictionary_default_accents)
else:
    # Получение цветовой схемы из файла
    dic_colors = ''
    with open(FILE_SETTINGS_COLOR, 'r') as file_accent:
        for i in file_accent.readlines():
            dic_colors = i
        file_accent.close()
    dictionary_default_accents = eval(dic_colors)
# Ключи словаря с цветами добавляются в массив
massive_colors = []
for accent in dictionary_default_accents:
    massive_colors.append(accent)
# Цвета в терминале
ACCENT_1 = format_hex_color(dictionary_default_accents[massive_colors[0]])
ACCENT_2 = format_hex_color(dictionary_default_accents[massive_colors[1]])
ACCENT_3 = format_hex_color(dictionary_default_accents[massive_colors[2]])
ACCENT_4 = format_hex_color(dictionary_default_accents[massive_colors[3]])
ACCENT_5 = format_hex_color(dictionary_default_accents[massive_colors[4]])
GREEN = format_hex_color('#6B8E4E')
RED = format_hex_color('#C70039')


# <<< ------- ДЕЙСТВИЯ С СИСТЕМОЙ ------- >>>
def system_action(action):
    """ Системные действия (выполнение действия) """
    if action == 'restart':
        system_action('clear')
        template_warning_message(GREEN, '--- RESTART ---')
        sleep(.1)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    if action == 'quit':
        template_some_message(ACCENT_3, '--- ELBA CLOSED ---')
        write_log("ELBA", "QUIT")
        quit()
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
        Поддержка синтаксиса командных оболочек Linux, MacOS и Windows
        (возвращение аргументов к действиям)
    """
    return {
        'copy_dir': lambda: 'xcopy /y /o /e ' if os.name == 'nt' else 'cp -r ',
        'rm_dir': lambda: 'rmdir ' if os.name == 'nt' else 'rm -r ',
        'copy_file': lambda: 'copy ' if os.name == 'nt' else 'cp ',
        'move': lambda: 'move ' if os.name == 'nt' else 'mv ',
        'rm': lambda: 'del ' if os.name == 'nt' else 'rm '
    }.get(action)()


def authentication_check(first_start=False, after_update=False):
    """ Проверка программы на подлинность """
    from werkzeug.security import generate_password_hash, check_password_hash

    def bin_reading_modules():
        """ Чтение модулей и запись в строку подряд """
        string_all_modules = ''
        not_in_list_of_modules = ['main.py', 'update_obs.py']
        # Добавление в хэш главного файла и модуля обновлений
        for item in not_in_list_of_modules:
            with open(item, 'rb') as binary_main:
                string_all_modules += str(binary_main.readlines())
        # Прокрутка имеющихся модулей
        for module in stock_modules:
            with open(module, 'rb') as binary_module:
                string_all_modules += str(binary_module.readlines())
                binary_module.close()
        return string_all_modules

    def create_signature():
        # Чтение имеющихся модулей
        reading_all_modules_for_sign = bin_reading_modules()
        hash_module = generate_password_hash(reading_all_modules_for_sign)
        with open(FILE_WITH_SHA256, 'w') as sha256:
            sha256.write(hash_module)
            sha256.close()
        system_action('clear')
        template_some_message(GREEN, 'Program signature created')
        sleep(2)
        system_action('clear')

    write_log('Authentication check', 'START')
    if os.path.exists(FILE_WITH_SHA256) is False:
        write_log('Not verified', 'WAIT')
        template_some_message(RED, 'It is impossible to establish the authenticity of the program')
        sleep(1)
        change_continue_or_not = template_question('Continue?')
        if change_continue_or_not == 'y':
            write_log('Not verified: Setting current', 'OK')
            # Прокрутка имеющихся модулей
            create_signature()
        else:
            system_action('clear')
            template_some_message(RED, 'REFUSAL')
            write_log('Not confirmed', 'QUIT')
            quit()
    else:
        # Чтение имеющихся модулей
        reading_all_modules = bin_reading_modules()
        # Чтение хеша
        with open(FILE_WITH_SHA256, 'r') as hash_modules:
            saved_hash_modules = hash_modules.readline()
        # Проверка на подлинность
        check = check_password_hash(saved_hash_modules, str(reading_all_modules))
        if (check or after_update) is False:
            template_some_message(RED, 'The authenticity of the program is not installed')
            sleep(2)
            quit()
        if first_start:
            system_action('clear')
            template_some_message(GREEN, 'Authenticated')
            sleep(1)
            system_action('clear')
        if after_update:
            create_signature()


def download_from_repository():
    """ Загрузка и установка из репозитория модуля обновлений """
    os.system(REPOSITORY)
    module_update = 'update_obs.py'
    system_action('clear')
    if os.path.exists(module_update) is False:
        os.system(get_peculiarities_system('copy_file') + f' elba/{module_update} .')
        system_action('restart')


def write_log(cause, status):
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
            data.close()

    log_data = open(FILE_LOG, mode="a", encoding='utf-8')
    log_writer = DictWriter(log_data, fieldnames=FIELDS_LOG_FILE, delimiter=';')
    log_writer.writerow({
        FIELDS_LOG_FILE[0]: __version__,     # Запись версии
        FIELDS_LOG_FILE[1]: get_time_now(),  # Запись даты и времени
        FIELDS_LOG_FILE[2]: status,          # Запись причины
        FIELDS_LOG_FILE[3]: cause            # Запись статуса
    })
    log_data.close()


def check_modules():
    """ Проверка наличия модулей программы """
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
        if cnt_missing_modules == 1:
            template_warning_message(RED, "--- Missing module ---")
        elif cnt_missing_modules > 1:
            template_warning_message(RED, "--- Missing modules ---")
        return 1


def use_token_for_authorization():
    pass


def point_of_entry():
    """ The main function responsible for the operation of the program """
    system_action('clear')
    write_log('-', '-')
    # info_obs.Information().save_modules_info()   # Запись информации о версии
    if os.path.exists(FOLDER_WITH_RESOURCES):  # При последующем запуске
        # authentication_check()  # Проверка на подлинность
        master_password = passwords_obs.ActionsWithPassword(None).verify_master_password(True)
        generic_key_from_file = security_obs.dec_aes(FILE_WITH_GENERIC_KEY, master_password)
        system_action('clear')
        datetime_obs.greeting(generic_key_from_file)
        write_log('Authorization', 'OK')
        functions_obs.ProgramFunctions(generic_key_from_file, 'resource').get_category_label()
        control_bus_obs.control_bus(generic_key_from_file)
    else:  # При первом запуске
        # authentication_check(first_start=True, after_update=False)  # Проверка на подлинность
        show_name_program()
        master_password = passwords_obs.ActionsWithPassword('master').get_password()
        generic_key = passwords_obs.ActionsWithPassword('generic').get_password()
        datetime_obs.greeting(generic_key)
        security_obs.enc_aes(FILE_WITH_GENERIC_KEY, generic_key, master_password)
        os.mkdir(FOLDER_WITH_RESOURCES)
        functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
        write_log('First launch', 'OK')
        control_bus_obs.control_bus(generic_key)


if __name__ == '__main__':
    system_action('clear')
    try:
        from update_obs import update
    except ModuleNotFoundError as update_obs_error:
        write_log(update_obs_error, 'FAIL')
        template_some_message(RED, '- Module "update" does not exist -')
        download_from_repository()

    try:
        import werkzeug.security
    except ModuleNotFoundError as error_module:
        write_log(error_module, 'CRASH')
        template_some_message(RED, f"MISSING: {error_module}")
        template_some_message(ACCENT_1, f"Please, install {str(error_module)[15:]}")
        quit()

    status_mis_mod = check_modules()    # Проверка модулей на наличие
    if status_mis_mod == 0:     # Если модули на месте
        import control_bus_obs
        import security_obs
        import datetime_obs
        import functions_obs
        import passwords_obs
        import logo_obs
        import info_obs
        import getpass_obs
        import rollback_obs

        try:
            point_of_entry()  # Точка входа в программу
        except Exception or NameError as random_error:
            from update_obs import trying_to_correct_an_error_in_execution
            trying_to_correct_an_error_in_execution(random_error)
        except KeyError:
            pass
        except KeyboardInterrupt:
            system_action('clear')
            template_some_message(ACCENT_3, '--- ELBA CLOSED ---')
            write_log("ELBA", "QUIT")
            quit()
    else:   # Попытка установить отсутствующие модули
        update()
