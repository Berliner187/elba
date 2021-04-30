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
from stdiomask import getpass


__version__ = 'v1.5.1.111'    # Version program


def show_name_program():
    print(blue,
          "\n || Password Manager and Keeper of Notes ||",
          __version__,
          "\n || Stable For Linux || \n || by Berliner187   ||", '\n' * 3, mc)
    elba()  # Вывод логотипа


def system_action(action):
    """ Restart Program or Clear terminal """
    if action == 'restart':
        os.execv(sys.executable, [sys.executable] + sys.argv)
    elif action == 'clear':
        os.system('cls' if os.name == 'nt' else 'clear')


# Цвета в терминале
yellow, blue, purple = "\033[33m", "\033[36m", "\033[35m"
green, red, mc = "\033[32m", "\033[31m", "\033[0m"

# Файлы для работы программы
main_folder = 'volare/'     # Mi fa volare
file_date_base = main_folder + "main_data.dat"     # Файл, в котором лежат пароли
file_lister = main_folder + ".lister.dat"   # Файл со строками
file_self_name = main_folder + ".self_name.dat"  # Файл с именем (никнеймом)
file_hash_password = main_folder + '.hash_password.dat'     # Файл с хэшем пароля
file_notes = main_folder + 'notes.csv'   # Файл с заметками
file_version = main_folder + '.version.log'  # Файл с версией программы

fields_for_logs = ['version', 'datetime', 'modules', 'status']     # Столбцы файла с логами
fields_for_main_data = ['resource', 'login', 'password']    # Столбцы для файла с ресурсами
fields_for_notes = ['name_note', 'note']    # Столбцы для файла с заметками

check_file_hash_password = os.path.exists(file_hash_password)
check_file_date_base = os.path.exists(file_date_base)    # Проверка этого файла на наличие
check_file_lister = os.path.exists(file_lister)   # Проверка этого файла на наличие
check_file_notes = os.path.exists(file_notes)   # Проверка на наличие файла с заметками

if os.path.exists(main_folder) == bool(False):
    os.mkdir(main_folder)

if check_file_notes == bool(False):     # Создание файла с заметками
    with open(file_notes, mode="a", encoding='utf-8') as file_for_notes:
        open_note = DictWriter(file_for_notes, fieldnames=fields_for_notes)
        open_note.writeheader()


def save_data_to_file(resource, login, password, master_password):
    """ Шифрование логина и пароля. Запись в csv-файл """
    with open(file_date_base, mode="a", encoding='utf-8') as data:
        writer = DictWriter(data, fieldnames=fields_for_main_data)
        if check_file_date_base == bool(False):
            writer.writeheader()    # Запись заголовков
        # Шифрование данных ресурса и запись в файл
        writer.writerow({
            fields_for_main_data[0]: enc_data(resource, master_password),
            fields_for_main_data[1]: enc_data(login, master_password),
            fields_for_main_data[2]: enc_data(password, master_password)})


def show_decryption_data(master_password):
    """ Показ всех сохраненных ресурсов """
    system_action('clear')
    with open(file_date_base, encoding='utf-8') as data:
        s = 0
        reader = DictReader(data, delimiter=',')
        print(yellow + '\n   --- Saved resources ---   ' + '\n'*3 + mc)
        for line in reader:
            decryption_res = dec_data(line["resource"], master_password)
            s += 1
            print(str(s) + '.', decryption_res)    # Decryption resource
        print(blue +
              '\n  - Enter "-r" to restart, "-x" to exit'
              '\n  - Enter "-a" to add new resource'
              '\n  - Enter "-c" to change master-password '
              '\n  - Enter "-d" to remove resource'
              '\n  - Enter "-n" to go to notes'
              '\n  - Enter "-u" to update program'
              '\n  - Enter "-z" to remove ALL data',
              yellow,
              '\n Select resource by number \n', mc)


def point_of_entry():    # Auth Confirm Password
    """ Получение мастер-пароля """
    show_name_program()     # Показывает название программы и выводит логотип
    master_password = getpass(yellow + '\n -- Your master-password: ' + mc)
    if master_password == 'x':  # Досрочный выход из программы
        quit()
    elif master_password == 'r':
        system_action('restart')
    elif master_password == 'a':    # Показ анимации
        animation()
    elif master_password == 'n':
        author()
    # Проверка хэша пароля
    with open(file_hash_password, 'r') as hash_pas_from_file:
        hash_password = check_password_hash(hash_pas_from_file.readline(), master_password)
        if hash_password == bool(False):    # Если хеши не совпадают
            print(red + '\n --- Wrong password --- ' + mc)
            sleep(1)
            system_action('restart')
        else:   # Если совпали
            return master_password


def change_type_of_password(resource, login, master_password):
    """ Выбор пароля: генерирование нового или сохранение пользовательского """
    print('\n',
          green + ' 1' + yellow + ' - Generation new password \n',
          green + ' 2' + yellow + ' - Save your password      \n', mc)

    change_type = int(input('Change (1/2): '))
    if change_type == 1:  # Генерирование пароля и сохранение в файл
        password = confirm_user_password('gen_new')
        save_data_to_file(resource, login, password, master_password)
    elif change_type == 2:  # Сохранение пользовательского пароля
        password = confirm_user_password('self')
        save_data_to_file(resource, login, password, master_password)
    else:   # Если ошибка выбора
        print(red + '  -- Error of change. Please, change again --  ' + mc)
        change_type_of_password(resource, login, master_password)
    system_action('clear')


def data_for_resource():
    """ Данные для сохранения (ресурс, логин) """
    system_action('clear')
    print(green, '\n   --- Add new resource ---   ', '\n' * 3, mc)
    resource = input(yellow + ' Resource: ' + mc)
    login = input(yellow + ' Login: ' + mc)
    return resource, login


def decryption_block(master_password):
    """ Цикл с выводом сохраненных ресурсов """

    def add_resource_data():
        resource, login = data_for_resource()
        change_type_of_password(resource, login, master_password)
        if check_file_date_base:
            show_decryption_data(master_password)
        else:
            system_action('restart')

    if check_file_date_base is False:   # При первом запуске
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
                print(blue, ' --- Program is closet --- \n', mc)
                sys.exit()  # Exit
            elif change_resource_or_actions == '-r':  # Условие перезапуска
                system_action('clear')  # Clearing terminal
                print('\n', green, ' -- Restart -- ', mc)
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
                print(red + '\n\n - Are you sure you want to delete all data? - ' + mc)
                change_yes_or_no = input(yellow + ' - Remove ALL data? (y/n): ' + mc)
                if change_yes_or_no == 'y':
                    os.system('rm -r elba/')   # Удаление папки
                    system_action('clear')
                    quit()
                else:
                    pass
            else:
                with open(file_date_base, encoding='utf-8') as profiles:
                    reader = DictReader(profiles, delimiter=',')
                    s = 0
                    for line in reader:  # Iterating over lines file
                        s += 1
                        if s == int(change_resource_or_actions):
                            system_action('clear')
                            show_decryption_data(master_password)

                            def resource_template(type_data, value):
                                """ Шаблон вывода данных о ресурсе """
                                print(yellow, type_data + ':', 
                                    green, dec_data(line[value], master_password), mc)

                            resource_template('Resource', 'resource')
                            resource_template('Login   ', 'login')
                            resource_template('Password', 'password')
        except ValueError:
            show_decryption_data(master_password)   # Показ содежимого
        decryption_block(master_password)  # Рекусрия под-главной функции


def download_from_repository(): # Загрузка из репозитория модуля обновлений
    os.system('git clone https://github.com/Berliner187/elba')  # Репозиторий
    system_action('clear')
    if os.path.exists('update_obs.py') == bool(False):
        os.system('mv elba/update_obs.py .')
        os.system('rm -r elba/ -f')
        system_action('restart')


def launcher():
    """ The main function responsible for the operation of the program """
    if check_file_date_base == bool(False):
        show_name_program()
        print(blue,
              "\n  - Encrypt your passwords with one master-password -    "
              "\n  -           No resources saved. Add them!         -  \n"
              "\n ----                That's easy!                 ---- \n",
              red,
              "\n         Программа не поддерживает русский язык          ",
              yellow,
              '\n --              Создание мастер-пароля               -- '
              '\n --    Только не используйте свой банковский пароль,  -- '
              '\n          я не сильно вкладывался в безопасность         '
              '\n                     этой программы                      ', mc)

        master_password = confirm_user_password('master')  # Создание мастер-пароля
        greeting(master_password)  # Вывод приветствия
        sleep(.5)
        decryption_block(master_password)
        system_action('restart')
    else:
        # Если файл уже создан
        master_password = point_of_entry()  # Ввод пароля
        system_action('clear')  # Очистка терминала
        greeting(master_password)  # Вывод приветствия
        sleep(.5)
        system_action('clear')  # Очистка терминала
        show_decryption_data(master_password)       # Показ содержимого файла с ресурсами
        decryption_block(master_password)  # Старт цикла


if __name__ == '__main__':
    system_action('clear')
    try:
        from update_obs import update
    except ModuleNotFoundError as error:
        print(error)
        print('-----')
        print(red + ' - Module "update" does not exist - ' + mc)
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
        from confirm_password_obs import confirm_user_password

        try:
            from werkzeug.security import generate_password_hash, check_password_hash
        except ModuleNotFoundError:
            print(red + 'Missing module: ' + green + 'werkzeug' + mc)
            sleep(1)
            quit()

        launcher()  # Запуск главной направляющей функции

    except ModuleNotFoundError:
        print(red + ' - Error in import local modules -' + mc)
        sleep(1)
        update()

    except ValueError:
        print(red, '\n' + ' --- Critical error, program is restarted --- ', mc)
        sleep(1)
        system_action('clear')
        print(red + ' -- You can try to update the program -- \n' + mc)
        change = input(yellow + ' - Update? (y/n): ' + mc)
        if change == 'y':  # Если получает запрос от юзера
            update()
        system_action('restart')
