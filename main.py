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
import random
from time import sleep
from shutil import copyfile
from csv import DictReader, DictWriter


__version__ = 'v1.5.1.1'    # Version program


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
    elif action == 'either':
        os.system('cls' if os.name == 'nt' else 'clear')
        os.execv(sys.executable, [sys.executable] + sys.argv)


# Colours
yellow, blue, purple, green, mc, red = "\033[33m", "\033[36m", "\033[35m", "\033[32m", "\033[0m", "\033[31m"
# List of all symbols for password
symbols_for_password = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-='

# Files for work program
main_folder = 'volare/'     # Mi fa volare
file_date_base = main_folder + "main_data.dat"     # Файл, в котором лежат пароли
file_lister = main_folder + ".lister.dat"   # Файл со строками
file_self_name = main_folder + ".self_name.dat"  # Файл с именем (никнеймом)
file_hash_password = main_folder + '.hash_password.dat'     # Файл с хэшем пароля
file_notes = main_folder + 'notes.csv'   # Файл с заметками
file_version = main_folder + '.version.log'  # Файл с версией программы

fields_for_logs = ['version', 'datetime', 'modules', 'status']     # Столбцы файла с логами
fields_for_main_data = ['resource', 'login', 'password']
fields_for_notes = ['name_note', 'note']

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
              '\n  - Enter "-c" to change master-password ', red, 'NEW' + blue,
              '\n  - Enter "-d" to remove resource'
              '\n  - Enter "-n" to go to notes'
              '\n  - Enter "-u" to update program'
              '\n  - Enter "-z" to remove ALL data',
              yellow, 
              '\n Select resource by number \n', mc)


def point_of_entry():    # Auth Confirm Password
    """ Получение мастер-пароля """
    show_name_program()     # Показывает название программы и выводит логотип
    master_password = hide_password(yellow + '\n -- Your master-password: ' + mc)
    if master_password == 'x':  # Досрочный выход из программы
        quit()
    elif master_password == 'r':
        system_action('restart')
    # Проверка хэша пароля
    with open(file_hash_password, 'r') as hash_pas_from_file:
        hash_password = check_password_hash(hash_pas_from_file.readline(), master_password)
        if hash_password == bool(False):    # Если хеши не совпадают
            print(red + '\n --- Wrong password --- ' + mc)
            sleep(1)
            system_action('either')
        else:   # Если совпали
            return master_password


def confirm_user_password(type_pas):
    """ Подтвержение пользовательского пароля """
    def user_input_password():
        print(blue + '\n Minimum password length 8 characters' + mc)
        user_password = hide_password('\n Password: ')
        if user_password == 'x':
            quit()
        user_confirm_password = hide_password(' Confirm password: ')  # hide_password(' Confirm password: ')
        if user_password != user_confirm_password or len(user_password) < 8:
            print(red + '\n Error of confirm. Try again \n' + mc)
            user_input_password()
        else:
            return user_password

    def generation_new_password():
        """ Генерирование нового случайного пароля """
        length_new_pas = int(input(yellow + ' - Length password (Minimum 8): ' + mc))
        new_password = ''  # Empty password
        for pas_elem in range(length_new_pas):
            new_password += random.choice(symbols_for_password)  # Password Adding random symbols from lister
        if len(new_password) > 8:
            return new_password  # Возвращает пароль
        else:
            print(red + '\n Error of confirm. Try again \n' + mc)
            generation_new_password()

    # Условаия принятия и подтверждения пароля
    if type_pas == 'self':  # Собсвенный пароль для ресурса
        password = user_input_password()
        print(blue + ' - Your password success saved' + mc)
        sleep(1)
        return password
    elif type_pas == 'master':  # Мастер пароль
        master_password = user_input_password()
        # Проверка хеша пароля
        if check_file_hash_password == bool(False) and check_file_date_base == bool(False):  # Создание хэша
            hash_to_file = generate_password_hash(master_password)
            with open(file_hash_password, 'w') as hash_pas:
                hash_pas.write(hash_to_file)
                hash_pas.close()
            return master_password
        elif check_file_hash_password == bool(False) and check_file_date_base == bool(True):
            print(red + ' - Not confirmed - ' + mc)
            sleep(2)
            quit()
        elif check_file_date_base and check_file_hash_password == bool(True):
            return master_password
    elif type_pas == 'gen_new':     # Генерирование нового пароля
        password = generation_new_password()
        print(blue + ' - Your new password - ' + green + password + mc + ' - success saved' + mc)
        sleep(2)
        return password


def change_type_of_password(resource, login, master_password):
    """ Выбор пароля: генерирование нового или сохрание пользовательского """
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
    print(green, '\n   --- Add new resource ---   ', '\n' * 3, mc)  # Текст запроса ввода данных о ресурсе
    resource = input(yellow + ' Resource: ' + mc)
    login = input(yellow + ' Login: ' + mc)
    return resource, login


def decryption_block(master_password):
    """ Show resources and decrypt them with keys """
    def add_resource_data():
        if check_file_date_base == bool(False):
            resource, login = data_for_resource()
            change_type_of_password(resource, login, master_password)
            system_action('restart')
        else:
            resource, login = data_for_resource()  # Ввод данных для ресурса
            change_type_of_password(resource, login, master_password)
            show_decryption_data(master_password)

    if check_file_date_base == bool(True):
        # Decryption mechanism
        change_resource_or_actions = input('\n Change: ')
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
                system_action('either')  # Restart program
            elif change_resource_or_actions == '-c':
                system_action('clear')
                # Сверяются хеши паролей
                confirm_master_password = hide_password(yellow + ' -- Enter your master-password: ' + mc)
                open_file_with_hash = open(file_hash_password).readline()
                check_master_password = check_password_hash(open_file_with_hash, confirm_master_password)

                if check_master_password == bool(False):
                    print(red + '\n --- Wrong password --- ' + mc)
                    sleep(1)
                    system_action('either')
                else:
                    print('[ ' + green + 'OK' + mc + ' ]')
                    sleep(.6)
                    system_action('clear')
                    print(blue + '\n Pick a new master-password \n' + mc)
                    new_master_password = confirm_user_password('master')
                    cnt = 0
                    with open(file_date_base, encoding='utf-8') as saved_resource:  # Выгружается старый файл
                        reader_resources = DictReader(saved_resource, delimiter=',')
                        mas_res, mas_log, mas_pas = [], [], []
                        new_file_data_base = 'new_file_data_base.dat'
                        for item in reader_resources:
                            cnt += 1    # Счетчик для нового файла
                            # Дешифрование старым паролем
                            dec_res = dec_data(item["resource"], master_password)
                            dec_log = dec_data(item["login"], master_password)
                            dec_pas = dec_data(item["password"], master_password)

                            # Шифрование новым паролем
                            enc_res = enc_data(dec_res, new_master_password)
                            enc_log = enc_data(dec_log, new_master_password)
                            enc_pas = enc_data(dec_pas, new_master_password)

                            # Добавление зашифрованных данных в массивы
                            mas_res.append(enc_res)
                            mas_log.append(enc_log)
                            mas_pas.append(enc_pas)

                    with open(new_file_data_base, mode="a", encoding='utf-8') as data:  # Запись в новый файл
                        new_writer = DictWriter(data, fieldnames=fields_for_main_data)
                        new_writer.writeheader()
                        for i in range(cnt):
                            new_writer.writerow({
                                'resource': mas_res[i],
                                'login': mas_log[i],
                                'password': mas_pas[i]
                            })
                    copyfile(new_file_data_base, file_date_base)    # Перезапись старого файла новым
                    os.system('rm ' + new_file_data_base)   # Удаление нового файла

                    new_hash = generate_password_hash(new_master_password)
                    with open(file_hash_password, 'w') as hash_pas:
                        hash_pas.write(new_hash)
                        hash_pas.close()

                system_action('restart')

            elif change_resource_or_actions == '-d':    # Удаление ресурса
                delete_resource()
                show_decryption_data(master_password)  # Вывод ресурсов
            elif change_resource_or_actions == '-n':    # Добавление зашифрованных заметок
                notes(master_password)
            elif change_resource_or_actions == '-z':    # Удаление всех данных пользователя
                system_action('clear')
                print(red + '\n\n - Are you sure you want to delete all data? - ' + mc)
                change_yes_or_no = input(yellow + ' - Remove ALL data? (y/n): ' + mc)   # Запрос подтверждения
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

                            def resource_template(type_data, value):  # Шаблон вывода данных о ресурсе
                                print(yellow, type_data + ':', green, dec_data(line[value], master_password), mc)

                            resource_template('Resource', 'resource')
                            resource_template('Login   ', 'login')
                            resource_template('Password', 'password')
        except ValueError:
            show_decryption_data(master_password)   # Показ содежимого
        decryption_block(master_password)  # Рекусрия под-главной функции
    else:
        add_resource_data()
        system_action('restart')


def launcher():
    """ The main function responsible for the operation of the program """
    if check_file_date_base == bool(False):   # Если файла нет, идет создание файла с ресурсами
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
        # Если файл уже создан, выводтся содержимое и дальнейшее взаимодействие с программой происходит тут
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
        from logo_obs import elba
        from enc_obs import enc_data, dec_data
        from datetime_obs import greeting
        from stars_obs import hide_password
        from update_obs import update
        from del_resource_obs import delete_resource
        from notes_obs import notes
        try:
            from werkzeug.security import generate_password_hash, check_password_hash
        except ModuleNotFoundError:
            print(red + 'Missing module' + mc)
            sleep(1)
            quit()

        launcher()  # Запуск главной направляющей функции
    except ModuleNotFoundError:
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
