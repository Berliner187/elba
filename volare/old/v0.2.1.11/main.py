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


__version__ = 'v0.2.1.11'    # Version program


def show_name_program():
    print(BLUE,
          "\n || Password Manager and Keeper of Notes ||",
          "\n || Delta For Linux || "
          "\n || by Berliner187  || ", YELLOW,
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
    os.system('rmdir ' + some_folder if os.name == 'nt'
    else 'rm -r ' + some_folder + ' -f')


def template_some_message(color, message):
    print(color, '\n\n', message, DEFAULT_COLOR)


# Цвета в терминале
YELLOW, BLUE, PURPLE = "\033[33m", "\033[36m", "\033[35m"
GREEN, RED, DEFAULT_COLOR = "\033[32m", "\033[31m", "\033[0m"

# Константы
FOLDER_ELBA = 'elba/'
FOLDER_WITH_DATA = 'volare/'     # Mi fa volare
FOLDER_WITH_RESOURCES = FOLDER_WITH_DATA + "resources/"
FOLDER_WITH_NOTES = FOLDER_WITH_DATA + 'notes/'   # Файл с заметками
old_elba = FOLDER_WITH_DATA + 'old/'  # Старые версии программы
FOLDERS = [FOLDER_WITH_DATA, FOLDER_WITH_NOTES]

FILE_RESOURCE = 'resource.dat'
FILE_LOGIN = 'login.dat'
FILE_PASSWORD = 'password.dat'

FILE_NOTE_NAME = 'name_note.dat'
FILE_NOTE_ITSELF = 'note_itself.dat'

FILE_USER_NAME = FOLDER_WITH_DATA + ".self_name.dat"  # Файл с никнеймом
FILE_WITH_HASH = FOLDER_WITH_DATA + '.hash_password.dat'  # Файл с хэшем пароля
FILE_LOG = FOLDER_WITH_DATA + '.file.log'  # Файл с версией программы

# Модули для работы программы
stock_modules = ['datetime_obs.py', 'enc_obs.py', 'logo_obs.py',
                 'del_resource_obs.py', 'notes_obs.py', 'get_size_obs.py',
                 'change_password_obs.py', 'actions_with_password_obs.py']

# Столбцы файла с логами
fields_for_log = ['version', 'date', 'cause', 'status']

# Проверка файлов на наличие
CHECK_FILE_WITH_HASH = os.path.exists(FILE_WITH_HASH)
CHECK_FILE_FOR_RESOURCE = os.path.exists(FOLDER_WITH_RESOURCES)

REPOSITORY = 'git clone https://github.com/Berliner187/elba -b delta'


for folder in FOLDERS:
    if os.path.exists(folder) is False:
        os.mkdir(folder)


def point_of_entry():   # Точка входа в систему
    """ Получение мастер-пароля """

    def template_wrong_message(value_left):
        print(RED, '\n  ---  Wrong password --- ',
              BLUE, "\n\n Attempts left:", RED, value_left, DEFAULT_COLOR)
        sleep(1)

    def get_master_password():
        show_name_program()     # Выводит название и логотип
        user_master_password = 'kozak022'#getpass(
            # YELLOW + '\n -- Your master-password: ' + DEFAULT_COLOR
        # )
        if user_master_password == 'x':  # Досрочный выход из программы
            quit()
        elif user_master_password == 'r':
            system_action('restart')
        elif user_master_password == 'a':    # Показ анимации
            animation()
        elif user_master_password == 'n':
            author()
        return user_master_password

    master_password = get_master_password()

    # Проверка хэша пароля
    with open(FILE_WITH_HASH, 'r') as hash_pas_from_file:
        hash_password = check_password_hash(hash_pas_from_file.readline(), master_password)
    cnt_left = 3    # Счет оставшихся попыток

    if hash_password is False:    # Если хеши не совпадают
        template_wrong_message(cnt_left)
        while hash_password is False:
            cnt_left -= 1
            system_action('clear')
            master_password = get_master_password()
            file_hash = open(FILE_WITH_HASH)
            hash_password = check_password_hash(file_hash.readline(), master_password)
            if cnt_left == 0:
                system_action('clear')
                print(RED + " -- Limit is exceeded -- " + DEFAULT_COLOR)
                sleep(2**10)
                quit()
            if hash_password:
                return master_password
            else:
                template_wrong_message(cnt_left)
    else:
        return master_password


def decryption_block(master_password):
    """ Цикл с выводом сохраненных ресурсов """

    def add_resource_data():
        """ Данные для сохранения (ресурс, логин) """
        system_action('clear')
        print(GREEN, '\n   --- Add new resource ---   ', '\n' * 3, DEFAULT_COLOR)
        resource = input(YELLOW + ' Resource: ' + DEFAULT_COLOR)
        login = input(YELLOW + ' Login: ' + DEFAULT_COLOR)
        choice_generation_or_save_self_password(resource, login, master_password)
        if CHECK_FILE_FOR_RESOURCE:
            show_decryption_data(master_password, 'resource')
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

            elif change_resource_or_actions == '-u':    # Обновление программы
                system_action('clear')
                update()
                show_decryption_data(master_password, 'resource')

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

            elif change_resource_or_actions == '-c':    # Смена мастер-пароля
                change_master_password()

            elif change_resource_or_actions == '-d':    # Удаление ресурса
                delete_resource('resource')
                show_decryption_data(master_password, 'resource')

            elif change_resource_or_actions == '-n':    # Добавление заметок
                notes(master_password)

            elif change_resource_or_actions == '-z':    # Удаление всех данных
                system_action('clear')
                template_some_message(RED, ' - Are you sure you want to delete all data? - ')
                change_yes_or_no = input(YELLOW + ' - Remove ALL data? (y/n): ' + DEFAULT_COLOR)
                if change_yes_or_no == 'y':
                    template_remove_folder(FOLDER_ELBA)
                    system_action('clear')
                    quit()

            elif change_resource_or_actions == '-s':
                from get_size_obs import size_all, get_versions
                get_versions()
                size_all()
                decryption_block(master_password)

            elif change_resource_or_actions == '-l':
                system_action("clear")
                print(GREEN + "\n Log program from file \n" + DEFAULT_COLOR)
                log_data = open(FILE_LOG, 'r')
                reader_log = DictReader(log_data, delimiter=';')
                for line in reader_log:
                    print(
                        line[fields_for_log[0]],
                        line[fields_for_log[1]],
                        line[fields_for_log[2]],
                        line[fields_for_log[3]]
                    )
                print(YELLOW + " - Press Enter to exit - " + DEFAULT_COLOR)

            elif change_resource_or_actions == '-dm':  # Удаление кэша
                template_remove_folder('rm -r __pycache__/')
                system_action('clear')
                print(GREEN + "\n" * 3, "    Success delete cache" + DEFAULT_COLOR)
                sleep(1)
                system_action('restart')

            elif change_resource_or_actions == '-o':    # Установка старой сохраненной версии
                if os.path.exists(old_elba) is False:
                    print(YELLOW + ' - No versions saved - ' + DEFAULT_COLOR)
                else:
                    install_old_saved_version()
                    system_action('restart')

            else:
                s = 0
                for resource_in_folder in os.listdir(FOLDER_WITH_RESOURCES):  # Вывод данных ресурса
                    s += 1
                    if s == int(change_resource_or_actions):
                        system_action('clear')
                        show_decryption_data(master_password, 'resource')

                        path_to_resource = FOLDER_WITH_RESOURCES + resource_in_folder
                        resource_from_file = path_to_resource + '/' + FILE_RESOURCE
                        login_from_file = path_to_resource + '/' + FILE_LOGIN
                        password_from_file = path_to_resource + '/' + FILE_PASSWORD

                        def template_print_decryption_data(data_type, value):
                            print(BLUE, data_type, YELLOW, dec_aes(value, master_password), DEFAULT_COLOR)

                        template_print_decryption_data(
                            'Resource --->', resource_from_file)
                        template_print_decryption_data(
                            'Login ------>', login_from_file)
                        template_print_decryption_data(
                            'Password --->', password_from_file)

        except ValueError:
            show_decryption_data(master_password, 'resource')   # Показ содежимого
        decryption_block(master_password)  # Рекусрия под-главной функции


def download_from_repository():
    """ Загрузка и установка из репозитория модуля обновлений """
    os.system(REPOSITORY)
    system_action('clear')
    if os.path.exists('update_obs.py') is False:
        os.system('mv elba/update_obs.py .')
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
            fields_for_log[1]: get_date(),      # Запись даты и времени
            fields_for_log[2]: cause,           # Запись причины
            fields_for_log[3]: status           # Запись статуса
        })


def launcher():
    """ The main function responsible for the operation of the program """
    if os.path.exists(FILE_LOG) is False:
        with open(FILE_LOG, mode="a", encoding='utf-8') as data:
            logs_writer = DictWriter(data, fieldnames=fields_for_log, delimiter=';')
            logs_writer.writeheader()
        write_log('First launch', 'OK')

    if CHECK_FILE_FOR_RESOURCE is False:
        # Если нет ресурсов
        os.mkdir(FOLDER_WITH_RESOURCES)
        show_name_program()
        print(BLUE,
              "\n  - Encrypt your passwords with one master-password -    "
              "\n  -           No resources saved. Add them!         -  \n"
              "\n ----                That's easy!                 ---- \n",
              RED,
              "\n          Программа не поддерживает русский язык         ",
              YELLOW,
              '\n --              Pick a master-password               -- '
              '\n --    Только не используйте свой банковский пароль,  -- '
              '\n          я не сильно вкладывался в безопасность         '
              '\n                     этой программы                      ',
              DEFAULT_COLOR)

        master_password = actions_with_password('master')  # Создание мастер-пароля
        greeting(master_password, False)  # Вывод приветствия
        sleep(.5)
        decryption_block(master_password)
        write_log('---', 'OK')
        system_action('restart')
    else:
        # Если есть ресурсы
        master_password = point_of_entry()
        system_action('clear')
        greeting(master_password, False)
        sleep(.5)
        system_action('clear')
        write_log('Subsequent launch', 'OK')
        show_decryption_data(master_password, 'resource')
        decryption_block(master_password)


if __name__ == '__main__':
    system_action('clear')
    try:
        from update_obs import update, install_old_saved_version
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
        template_some_message(
            YELLOW, "Please, install module/modules with PIP and restart the program"
        )
        quit()

    try:
        # Локальные модули
        from logo_obs import elba, animation, author
        from datetime_obs import greeting
        from del_resource_obs import delete_resource
        from notes_obs import notes
        from change_password_obs import change_master_password
        from actions_with_password_obs import actions_with_password, choice_generation_or_save_self_password
        from enc_obs import show_decryption_data, dec_aes

        launcher()  # Запуск главной направляющей функции

    except ModuleNotFoundError as error:
        print(error)
        print(RED + ' - Error in import modules -' + DEFAULT_COLOR)
        write_log(error, 'CRASH MODULES')
        sleep(.5)
        update()

    except ValueError as error:
        print(error)
        write_log(error, 'CRITICAL CRASH')
        print(RED, '\n --- Critical error, program is restarted --- ', DEFAULT_COLOR)
        sleep(1)
        system_action('clear')
        # Попытка обновиться, если возникает ошибка
        print(RED + ' -- You can try roll back -- \n' + DEFAULT_COLOR)
        change = input(YELLOW + ' - Roll back? (y/n): ' + DEFAULT_COLOR)
        if change == 'y':
            install_old_saved_version()
        system_action('restart')
