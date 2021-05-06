#!/usr/bin/env python3

"""
    Password Manager Stable For Linux (SFL)
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


__version__ = 'BETA v0.1.0.3'    # Version program


def show_name_program():
    print(BLUE,
          "\n || Password Manager and Keeper of Notes ||",
          "\n || Stable For Linux || "
          "\n || by Berliner187   || ", 
          __version__,
          '\n' * 3, DEFAULT_COLOR)
    elba()  # Вывод логотипа


def system_action(action):
    """ Restart Program or Clear terminal """
    if action == 'restart':
        os.execv(sys.executable, [sys.executable] + sys.argv)
    elif action == 'clear':
        os.system('cls' if os.name == 'nt' else 'clear')


# Цвета в терминале
YELLOW, BLUE, PURPLE = "\033[33m", "\033[36m", "\033[35m"
GREEN, RED, DEFAULT_COLOR = "\033[32m", "\033[31m", "\033[0m"

# Файлы для работы программы
FOLDER_WITH_DATA = 'volare/'     # Mi fa volare
FILE_FOR_RESOURCE = FOLDER_WITH_DATA + "main_data.dat"     # Файл, в котором лежат пароли
FILE_USER_NAME = FOLDER_WITH_DATA + ".self_name.dat"  # Файл с именем (никнеймом)
FILE_WITH_HASH = FOLDER_WITH_DATA + '.hash_password.dat'     # Файл с хэшем пароля
FILE_FOR_NOTES = FOLDER_WITH_DATA + 'notes.csv'   # Файл с заметками
FILE_LOG = FOLDER_WITH_DATA + '.file.log'  # Файл с версией программы

fields_for_log = ['version', 'date', 'cause', 'status']     # Столбцы файла с логами
fields_for_main_data = ['resource', 'login', 'password']    # Столбцы для файла с ресурсами
fields_for_notes = ['name_note', 'note']    # Столбцы для файла с заметками

# Проверка файлов на наличие
CHECK_FILE_WITH_HASH = os.path.exists(FILE_WITH_HASH)
CHECK_FILE_FOR_RESOURCE = os.path.exists(FILE_FOR_RESOURCE)

REPOSITORY = 'git clone https://github.com/Berliner187/elba'

if os.path.exists(FOLDER_WITH_DATA) == bool(False):  # Папка с данными программы
    os.mkdir(FOLDER_WITH_DATA)

if os.path.exists(FILE_FOR_NOTES) == bool(False):     # Создание файла с заметками
    with open(FILE_FOR_NOTES, mode="a", encoding='utf-8') as file_for_notes:
        open_note = DictWriter(file_for_notes, fieldnames=fields_for_notes)
        open_note.writeheader()


def save_data_to_file(resource, login, password, master_password):
    """ Шифрование логина и пароля. Запись в csv-файл """
    with open(FILE_FOR_RESOURCE, mode="a", encoding='utf-8') as data:
        writer = DictWriter(data, fieldnames=fields_for_main_data)
        if CHECK_FILE_FOR_RESOURCE == bool(False):
            writer.writeheader()    # Запись заголовков
        # Шифрование данных ресурса и запись в файл
        writer.writerow({
            fields_for_main_data[0]: enc_data(resource, master_password),
            fields_for_main_data[1]: enc_data(login, master_password),
            fields_for_main_data[2]: enc_data(password, master_password)})


def show_decryption_data(master_password):
    """ Показ всех сохраненных ресурсов """
    system_action('clear')
    with open(FILE_FOR_RESOURCE, encoding='utf-8') as data:
        s = 0
        reader = DictReader(data, delimiter=',')
        print(YELLOW + '\n   --- Saved resources ---   ' + '\n'*3 + DEFAULT_COLOR)
        for line in reader:
            decryption_res = dec_data(line["resource"], master_password)
            s += 1
            print(str(s) + '.', decryption_res)    # Decryption resource
        print(BLUE +
              '\n  - Enter "-r" to restart, "-x" to exit'
              '\n  - Enter "-a" to add new resource'
              '\n  - Enter "-c" to change master-password '
              '\n  - Enter "-d" to remove resource'
              '\n  - Enter "-n" to go to notes'
              '\n  - Enter "-u" to update program'
              '\n  - Enter "-z" to remove ALL data',
              YELLOW,
              '\n Select resource by number \n', DEFAULT_COLOR)


def point_of_entry():    # Auth Confirm Password
    """ Получение мастер-пароля """
    show_name_program()     # Показывает название программы и выводит логотип
    master_password = getpass(YELLOW + '\n -- Your master-password: ' + DEFAULT_COLOR)
    if master_password == 'x':  # Досрочный выход из программы
        quit()
    elif master_password == 'r':
        system_action('restart')
    elif master_password == 'a':    # Показ анимации
        animation()
    elif master_password == 'n':
        author()
    # Проверка хэша пароля
    with open(FILE_WITH_HASH, 'r') as hash_pas_from_file:
        hash_password = check_password_hash(hash_pas_from_file.readline(), master_password)
        if hash_password == bool(False):    # Если хеши не совпадают
            print(RED + '\n --- Wrong password --- ' + DEFAULT_COLOR)
            sleep(1)
            system_action('restart')
        else:   # Если совпали
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


def data_for_resource():
    """ Данные для сохранения (ресурс, логин) """
    system_action('clear')
    print(GREEN, '\n   --- Add new resource ---   ', '\n' * 3, DEFAULT_COLOR)
    resource = input(YELLOW + ' Resource: ' + DEFAULT_COLOR)
    login = input(YELLOW + ' Login: ' + DEFAULT_COLOR)
    return resource, login


def decryption_block(master_password):
    """ Цикл с выводом сохраненных ресурсов """

    def add_resource_data():
        resource, login = data_for_resource()
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
            elif change_resource_or_actions == '-x':  # Условие выхода
                system_action('clear')  # Clearing terminal
                print(BLUE, ' --- Program is closet --- \n', DEFAULT_COLOR)
                quit()  # Exit
            elif change_resource_or_actions == '-r':  # Условие перезапуска
                system_action('clear')  # Clearing terminal
                print('\n', GREEN, ' -- Restart -- ', DEFAULT_COLOR)
                sleep(.4)
                system_action('restart')  # Restart program
            elif change_resource_or_actions == '-c':
                change_master_password()
            elif change_resource_or_actions == '-d':    # Удаление ресурса
                delete_resource()
                show_decryption_data(master_password)  # Вывод ресурсов
            elif change_resource_or_actions == '-n':    # Добавление зашифрованных заметок
                notes(master_password)
            elif change_resource_or_actions == '-z':    # Удаление всех данных пользователя
                system_action('clear')
                print(RED + '\n\n - Are you sure you want to delete all data? - ' + DEFAULT_COLOR)
                change_yes_or_no = input(YELLOW + ' - Remove ALL data? (y/n): ' + DEFAULT_COLOR)
                if change_yes_or_no == 'y':
                    os.system('rm -r elba/')   # Удаление папки
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

            else:
                with open(FILE_FOR_RESOURCE, encoding='utf-8') as profiles:
                    reader = DictReader(profiles, delimiter=',')
                    s = 0
                    for line in reader:  # Iterating over lines file
                        s += 1
                        if s == int(change_resource_or_actions):
                            system_action('clear')
                            show_decryption_data(master_password)

                            def resource_template(type_data, value):
                                """ Шаблон вывода данных о ресурсе """
                                print(YELLOW,
                                      type_data + ':',
                                      GREEN, dec_data(line[value], master_password),
                                      DEFAULT_COLOR)

                            resource_template('Resource', 'resource')
                            resource_template('Login   ', 'login')
                            resource_template('Password', 'password')
        except ValueError:
            show_decryption_data(master_password)   # Показ содежимого
        decryption_block(master_password)  # Рекусрия под-главной функции


def download_from_repository():
    """ Загрузка и установка из репозитория модуля обновлений """
    os.system(REPOSITORY)
    system_action('clear')
    if os.path.exists('update_obs.py') == bool(False):
        os.system('mv elba/update_obs.py .')
        os.system('rm -r elba/ -f')
        system_action('restart')


def launcher():
    """ The main function responsible for the operation of the program """
    if os.path.exists(FILE_LOG) is False:
        with open(FILE_LOG, mode="a", encoding='utf-8') as data:
            logg_writer = DictWriter(data, fieldnames=fields_for_log, delimiter=';')
            logg_writer.writeheader()
        write_log('First Start', 'START')

    if CHECK_FILE_FOR_RESOURCE is False:
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
        greeting(master_password)  # Вывод приветствия
        sleep(.5)
        decryption_block(master_password)
        write_log('---', 'OK')
        system_action('restart')
    else:
        # Если файл уже создан
        master_password = point_of_entry()  # Ввод пароля
        system_action('clear')  # Очистка терминала
        greeting(master_password)  # Вывод приветствия
        sleep(.5)
        system_action('clear')  # Очистка терминала
        write_log('Subsequent launch', 'OK')
        show_decryption_data(master_password)       # Показ содержимого файла с ресурсами
        decryption_block(master_password)  # Старт цикла


if __name__ == '__main__':
    system_action('clear')
    try:
        from update_obs import update
    except ModuleNotFoundError as error:
        write_log(error, 'CRASH')
        print(RED + ' - Module "update" does not exist - ' + DEFAULT_COLOR)
        sleep(1)
        download_from_repository()

    try:
        # Локальные модули
        from logo_obs import elba, animation, author
        from enc_obs import enc_data, dec_data
        from datetime_obs import greeting
        from del_resource_obs import delete_resource
        from notes_obs import notes
        from change_password_obs import change_master_password
        from confirm_password_obs import actions_with_password
        from logs_obs import write_log

        try:
            from werkzeug.security import generate_password_hash, check_password_hash
            from stdiomask import getpass
        except ModuleNotFoundError as error:
            write_log(error, 'CRASH')
            print(
                RED + 'Missing module: ' +
                GREEN + 'werkzeug or stdiomask' +
                DEFAULT_COLOR
            )
            sleep(1)
            quit()

        launcher()  # Запуск главной направляющей функции

    except ModuleNotFoundError as error:
        print(RED + ' - Error in import local modules -' + DEFAULT_COLOR)
        write_log(error, 'CRASH')
        sleep(.5)
        update()

    except ValueError as error:
        write_log(error, 'CRASH')
        print(RED, '\n' + ' --- Critical error, program is restarted --- ', DEFAULT_COLOR)
        sleep(1)
        system_action('clear')
        # Попытка обновиться, если возникает ошибка
        print(RED + ' -- You can try to update the program -- \n' + DEFAULT_COLOR)
        change = input(YELLOW + ' - Update? (y/n): ' + DEFAULT_COLOR)
        if change == 'y':
            update()
        system_action('restart')
