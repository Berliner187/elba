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


__version__ = 'DELTA v0.2.1.5'    # Version program


def show_name_program():
    print(BLUE,
          "\n || Password Manager and Keeper of Notes ||",
          "\n || Beta For Linux || "
          "\n || by Berliner187 || ", YELLOW,
          "\n\n || Ferga Kangaroo || ", BLUE,
          __version__)
    elba()  # Вывод логотипа


def system_action(action):
    """ Restart Program or Clear terminal """
    if action == 'restart':
        os.execv(sys.executable, [sys.executable] + sys.argv)
    if action == 'clear':
        os.system('cls' if os.name == 'nt' else 'clear')


def template_remove_folder(some_folder):
    os.system('rmdir ' + some_folder if os.name == 'nt' else 'rm -r ' + some_folder + ' -f')


# Цвета в терминале
YELLOW, BLUE, PURPLE = "\033[33m", "\033[36m", "\033[35m"
GREEN, RED, DEFAULT_COLOR = "\033[32m", "\033[31m", "\033[0m"

# Константы
NEW_FOLDER_ELBA = 'elba/'
FOLDER_WITH_DATA = 'volare/'     # Mi fa volare
FOLDER_WITH_RESOURCES = FOLDER_WITH_DATA + "resources/"     # Папка с папками ресурсов
FOLDER_WITH_NOTES = FOLDER_WITH_DATA + 'notes/'   # Файл с заметками
FOLDERS = [FOLDER_WITH_DATA, FOLDER_WITH_NOTES]

FILE_RESOURCE = 'resource.dat'
FILE_LOGIN = 'login.dat'
FILE_PASSWORD = 'password.dat'

FILE_NOTE_ITSELF = 'note_itself.dat'

FILE_USER_NAME = FOLDER_WITH_DATA + ".self_name.dat"  # Файл с именем (никнеймом)
FILE_WITH_HASH = FOLDER_WITH_DATA + '.hash_password.dat'     # Файл с хэшем пароля
FILE_LOG = FOLDER_WITH_DATA + '.file.log'  # Файл с версией программы

fields_for_log = ['version', 'date', 'cause', 'status']     # Столбцы файла с логами
fields_for_main_data = ['resource', 'login', 'password']    # Столбцы для файла с ресурсами
fields_for_notes = ['name_note', 'note']    # Столбцы для файла с заметками

# Проверка файлов на наличие
CHECK_FILE_WITH_HASH = os.path.exists(FILE_WITH_HASH)
CHECK_FILE_FOR_RESOURCE = os.path.exists(FOLDER_WITH_RESOURCES)

REPOSITORY = 'git clone https://github.com/Berliner187/elba -b delta'


def path_to_resource_data(enc_resource):
    return FOLDER_WITH_RESOURCES + enc_resource


for folder in FOLDERS:
    if os.path.exists(folder) is False:
        os.mkdir(folder)


def save_data_to_file(resource, login, password, master_password):
    from enc_obs import enc_only_base64, enc_aes
    """ Шифрование логина и пароля. Запись в директорию с ресурсами """
    enc_name_folder = enc_only_base64(resource, master_password)
    enc_name_folder += '/'

    if os.path.exists(path_to_resource_data(enc_name_folder)) is False:
        os.mkdir(path_to_resource_data(enc_name_folder))

    resource_folder = path_to_resource_data(enc_name_folder)
    login_folder = path_to_resource_data(enc_name_folder)
    password_folder = path_to_resource_data(enc_name_folder)

    resource_file = resource_folder + FILE_RESOURCE
    login_file = login_folder + FILE_LOGIN
    password_file = password_folder + FILE_PASSWORD

    enc_aes(resource_file, resource, master_password)
    enc_aes(login_file, login, master_password)
    enc_aes(password_file, password, master_password)


def show_decryption_data(master_password):
    """ Показ всех сохраненных ресурсов """
    system_action('clear')
    print(PURPLE, "     ___________________________________")
    print(PURPLE, "    /\/| ", YELLOW, "\/                   \/", PURPLE, " |\/\ ")
    print(PURPLE, "   /\/\|", YELLOW, " \/  Saved resources  \/ ", PURPLE, "|/\/\ ", DEFAULT_COLOR)
    print(YELLOW, "           \/                   \/ ", DEFAULT_COLOR)
    print('\n'*5)

    s = 0
    for resource in os.listdir(FOLDER_WITH_RESOURCES):
        decryption_res = dec_only_base64(resource, master_password)
        s += 1
        print(PURPLE, str(s) + '.', YELLOW, decryption_res, DEFAULT_COLOR)    # Decryption resource
    print(BLUE +
          '\n  - Enter "-r" to restart, "-x" to exit'
          '\n  - Enter "-a" to add new resource'
          '\n  - Enter "-c" to change master-password'
          '\n  - Enter "-d" to remove resource',
          BLUE,
          RED, '\n  - Enter "-n" to go to notes            !',
          BLUE,
          '\n  - Enter "-u" to update program'
          '\n  - Enter "-z" to remove ALL data',
          YELLOW,
          '\n Select resource by number \n', DEFAULT_COLOR)


def point_of_entry():   # Точка входа в систему
    """ Получение мастер-пароля """

    def template_wrong_message(value_left):
        print(RED, '\n  ---  Wrong password --- ',
              BLUE, "\n\n Attempts left:", RED, value_left, DEFAULT_COLOR)
        sleep(1)

    def starter_elements(color, text):
        show_name_program()     # Выводит название и логотип
        master_password = getpass(color + '\n ' + text + DEFAULT_COLOR)
        if master_password == 'x':  # Досрочный выход из программы
            quit()
        elif master_password == 'r':
            system_action('restart')
        elif master_password == 'a':    # Показ анимации
            animation()
        elif master_password == 'n':
            author()
        return master_password

    master_password = starter_elements(YELLOW, ' -- Your master-password: ')

    # Проверка хэша пароля
    with open(FILE_WITH_HASH, 'r') as hash_pas_from_file:
        hash_password = check_password_hash(hash_pas_from_file.readline(), master_password)
    cnt_left = 3    # Счет оставшихся попыток

    if hash_password is False:    # Если хеши не совпадают
        template_wrong_message(cnt_left)
        while hash_password is False:
            cnt_left -= 1
            system_action('clear')
            master_password = starter_elements(YELLOW, ' -- Your master-password: ')
            file_hash = open(FILE_WITH_HASH)
            hash_password = check_password_hash(file_hash.readline(), master_password)
            if cnt_left == 0:
                system_action('clear')
                print(RED + " -- Limit is exceeded -- " + DEFAULT_COLOR)
                sleep(2**10)
                quit()
            if hash_password is True:
                return master_password
            else:
                template_wrong_message(cnt_left)
    else:
        return master_password


def change_type_of_password(resource, login, master_password):
    """ Выбор пароля: генерирование нового или сохранение пользовательского """
    print('\n',
          GREEN + ' 1' + YELLOW + ' - Generation new password \n',
          GREEN + ' 2' + YELLOW + ' - Save your password      \n', DEFAULT_COLOR)

    change_type = int(input('Change (1/2): '))
    if change_type == 1:  # Генерирование пароля и сохранение в файл
        password = actions_with_password('gen_new')
        save_data_to_file(resource, login, password, master_password)
    elif change_type == 2:  # Сохранение пользовательского пароля
        password = actions_with_password('self')
        save_data_to_file(resource, login, password, master_password)
    else:   # Если ошибка выбора
        print(RED + '  -- Error of change. Please, change again --  ' + DEFAULT_COLOR)
        change_type_of_password(resource, login, master_password)
    system_action('clear')


def decryption_block(master_password):
    """ Цикл с выводом сохраненных ресурсов """

    def add_resource_data():
        """ Данные для сохранения (ресурс, логин) """
        system_action('clear')
        print(GREEN, '\n   --- Add new resource ---   ', '\n' * 3, DEFAULT_COLOR)
        resource = input(YELLOW + ' Resource: ' + DEFAULT_COLOR)
        login = input(YELLOW + ' Login: ' + DEFAULT_COLOR)
        change_type_of_password(resource, login, master_password)
        if CHECK_FILE_FOR_RESOURCE:
            show_decryption_data(master_password)
        else:
            system_action('restart')

    if CHECK_FILE_FOR_RESOURCE is False:   # При первом запуске
        add_resource_data()
        system_action('restart')
    else:  # При последущих запусках программа работает тут
        change_resource_or_actions = input('\n Change: ')   # Выбор действия
        try:
            if change_resource_or_actions == '-a':  # Добавление нового ресурса
                add_resource_data()

            elif change_resource_or_actions == '-u':    # Обновление программы из репозитория
                system_action('clear')
                update()
                show_decryption_data(master_password)

            elif change_resource_or_actions == '-x':  # Выход
                system_action('clear')
                print(BLUE, ' --- Program is closet --- \n', DEFAULT_COLOR)
                write_log("Exit", "OK")
                quit()

            elif change_resource_or_actions == '-r':  # Перезапуск
                system_action('clear')
                print('\n', GREEN, ' -- Restart -- ', DEFAULT_COLOR)
                sleep(.4)
                system_action('restart')

            elif change_resource_or_actions == '-c':
                change_master_password()

            elif change_resource_or_actions == '-d':    # Удаление ресурса
                delete_resource()
                show_decryption_data(master_password)

            elif change_resource_or_actions == '-n':    # Добавление зашифрованных заметок
                notes(master_password)

            elif change_resource_or_actions == '-z':    # Удаление всех данных пользователя
                system_action('clear')
                print(RED + '\n\n - Are you sure you want to delete all data? - ' + DEFAULT_COLOR)
                change_yes_or_no = input(YELLOW + ' - Remove ALL data? (y/n): ' + DEFAULT_COLOR)
                if change_yes_or_no == 'y':
                    template_remove_folder(NEW_FOLDER_ELBA)
                    system_action('clear')
                    quit()

            elif change_resource_or_actions == '-s':
                from get_size_obs import size_all
                size_all()
                decryption_block(master_password)
            elif change_resource_or_actions == '-l':
                system_action("clear")
                print(GREEN + "\n Log program from file \n" + DEFAULT_COLOR)
                with open(FILE_LOG, 'r') as log_data:
                    reader_log = DictReader(log_data, delimiter=';')
                    for line in reader_log:
                        print(
                            line[fields_for_log[0]],
                            line[fields_for_log[1]],
                            line[fields_for_log[2]],
                            line[fields_for_log[3]]
                        )
                print(YELLOW + " - Press Enter to exit - " + DEFAULT_COLOR)
                
            elif change_resource_or_actions == '-i':    # Показ версий модулей
                from change_password_obs import __version__ as change_password_ver
                from confirm_password_obs import __version__ as confirm_password_ver
                from datetime_obs import __version__ as datetime_ver
                from del_resource_obs import __version__ as del_resource_ver
                from enc_obs import __version__ as enc_ver
                from get_size_obs import __version__ as get_size_ver
                from logo_obs import __version__ as logo_ver
                from notes_obs import __version__ as notes_ver
                from update_obs import __version__ as update_ver

                system_action('clear')
                print(GREEN, '\n  - Versions installed modules - \n', DEFAULT_COLOR)

                def template_version_module(module, version):
                    print(YELLOW, version, GREEN, module, DEFAULT_COLOR)

                template_version_module('program', __version__)
                template_version_module('change_password_obs', change_password_ver)
                template_version_module('confirm_password_obs', confirm_password_ver)
                template_version_module('datetime_obs', datetime_ver)
                template_version_module('del_resource_obs', del_resource_ver)
                template_version_module('enc_obs', enc_ver)
                template_version_module('get_size_obs', get_size_ver)
                template_version_module('logo_obs', logo_ver)
                template_version_module('notes_obs', notes_ver)
                template_version_module('update_obs', update_ver)

            elif change_resource_or_actions == '-dm':  # Удаление кэша
                template_remove_folder('rm -r __pycache__/')
                system_action('clear')
                print(GREEN + "\n" * 3, "    Success delete cache" + DEFAULT_COLOR)
                sleep(1)
                system_action('restart')

            else:
                s = 0
                for resource_in_folder in os.listdir(FOLDER_WITH_RESOURCES):  # Вывод данных ресурса
                    s += 1
                    if s == int(change_resource_or_actions):
                        system_action('clear')
                        show_decryption_data(master_password)

                        resource_from_file = FOLDER_WITH_RESOURCES + resource_in_folder + '/' + FILE_RESOURCE
                        login_from_file = FOLDER_WITH_RESOURCES + resource_in_folder + '/' + FILE_LOGIN
                        password_from_file = FOLDER_WITH_RESOURCES + resource_in_folder + '/' + FILE_PASSWORD

                        def template_print_decryption_data(data_type, value):
                            print(BLUE, data_type, YELLOW, dec_aes(value, master_password), DEFAULT_COLOR)

                        template_print_decryption_data('Resource --->', resource_from_file)
                        template_print_decryption_data('Login ------>', login_from_file)
                        template_print_decryption_data('Password --->', password_from_file)

        except ValueError:
            show_decryption_data(master_password)   # Показ содежимого
        decryption_block(master_password)  # Рекусрия под-главной функции


def download_from_repository():
    """ Загрузка и установка из репозитория модуля обновлений """
    os.system(REPOSITORY)
    system_action('clear')
    if os.path.exists('update_obs.py') == bool(False):
        os.system('mv elba/update_obs.py .')
        template_remove_folder('elba')
        system_action('restart')


def write_log(cause, status):
    """ Логирование """
    def get_date():      # Получение и форматирование текущего времени
        hms = datetime.datetime.today()  # Дата и время
        day, month, year = hms.day, hms.month, hms.year     # Число, месяц, год
        time_format = str(hms.hour) + ':' + str(hms.minute) + ':' + str(hms.second)
        date_format = str(day) + '.' + str(month) + '.' + str(year)
        total = str(time_format) + '-' + str(date_format)
        return ''.join(total)

    with open(FILE_LOG, mode="a", encoding='utf-8') as log_data:
        log_writer = DictWriter(log_data, fieldnames=fields_for_log, delimiter=';')
        if os.path.exists(FILE_LOG) is False:
            log_writer.writeheader()

        log_writer.writerow({
            fields_for_log[0]: __version__,     # Запись версии
            fields_for_log[1]: get_date(),     # Запись даты и времени
            fields_for_log[2]: cause,     # Запись причины
            fields_for_log[3]: status
        })  # Запись статуса


def launcher():
    """ The main function responsible for the operation of the program """
    if os.path.exists(FILE_LOG) is False:
        with open(FILE_LOG, mode="a", encoding='utf-8') as data:
            logs_writer = DictWriter(data, fieldnames=fields_for_log, delimiter=';')
            logs_writer.writeheader()
        write_log('First launch', 'OK')

    if CHECK_FILE_FOR_RESOURCE is False:
        os.mkdir(FOLDER_WITH_RESOURCES)
        show_name_program()
        print(BLUE,
              "\n  - Encrypt your passwords with one master-password -    "
              "\n  -           No resources saved. Add them!         -  \n"
              "\n ----                That's easy!                 ---- \n",
              RED,
              "\n         Программа не поддерживает русский язык          ",
              YELLOW,
              '\n --              Создание мастер-пароля               -- '
              '\n --    Только не используйте свой банковский пароль,  -- '
              '\n          я не сильно вкладывался в безопасность         '
              '\n                     этой программы                      ', DEFAULT_COLOR)

        master_password = actions_with_password('master')  # Создание мастер-пароля
        greeting(master_password, False)  # Вывод приветствия
        sleep(.5)
        decryption_block(master_password)
        write_log('---', 'OK')
        system_action('restart')
    else:
        # Если файл уже создан
        master_password = point_of_entry()  # Ввод пароля
        system_action('clear')  # Очистка терминала
        greeting(master_password, False)  # Вывод приветствия
        sleep(.5)
        system_action('clear')  # Очистка терминала
        write_log('Subsequent launch', 'OK')
        show_decryption_data(master_password)       # Показ содержимого файла с ресурсами
        decryption_block(master_password)  # Старт цикла


if __name__ == '__main__':
    system_action('clear')
    try:
        from update_obs import update
    except ModuleNotFoundError as update_obs_error:
        write_log(update_obs_error, 'CRASH UPDATE')
        print(RED + ' - Module "update" does not exist - ' + DEFAULT_COLOR)
        sleep(1)
        download_from_repository()

    try:
        from werkzeug.security import generate_password_hash, check_password_hash
        from stdiomask import getpass
    except ModuleNotFoundError as error_module:
        write_log(error_module, 'CRASH')
        print(RED + 'Error: \n' + str(error_module) + DEFAULT_COLOR)
        print('\n')
        print(YELLOW + "Please, install module/modules with PIP and restart the program" + DEFAULT_COLOR)
        sleep(1)
        quit()

    try:
        # Локальные модули
        from logo_obs import elba, animation, author
        from datetime_obs import greeting
        from del_resource_obs import delete_resource
        from notes_obs import notes
        from change_password_obs import change_master_password
        from confirm_password_obs import actions_with_password
        from enc_obs import enc_only_base64, dec_only_base64, enc_aes, dec_aes

        launcher()  # Запуск главной направляющей функции

    except ModuleNotFoundError as error:
        print(RED + ' - Error in import modules -' + DEFAULT_COLOR)
        write_log(error, 'CRASH MODULES')
        sleep(.5)
        update()

    except ValueError as error:
        write_log(error, 'CRITICAL CRASH')
        print(RED, '\n' + ' --- Critical error, program is restarted --- ', DEFAULT_COLOR)
        sleep(1)
        system_action('clear')
        # Попытка обновиться, если возникает ошибка
        print(RED + ' -- You can try to update the program -- \n' + DEFAULT_COLOR)
        change = input(YELLOW + ' - Update? (y/n): ' + DEFAULT_COLOR)
        if change == 'y':
            update()
        os.system('del' if os.name == 'nt' else 'rm')
        system_action('restart')
