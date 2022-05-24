# -*- coding: UTF-8 -*-

"""
    В этот модуль вынесены все действия с паролями
"""

from main import *

import security_obs
import logo_obs
import functions_obs
from getpass_obs import getpass

from time import sleep
import os
import re
import random

from werkzeug.security import generate_password_hash, check_password_hash


__version__ = '0.10-03'


cols = get_size_of_terminal()


def create_and_confirm_user_password():
    """ Создание и подтверждение пользовательского пароля """
    print(ACCENT_3, '— Minimum password length — 8 characters')
    print(ACCENT_3, '— Your password must contain lowercase letters')
    print(ACCENT_3, '— Your password must contain upper letters')
    print(ACCENT_3, '— Your password must contain numbers')
    print('\n')

    def template_red_messages(message):
        system_action('clear')
        print(f"{RED}\n\n - {message}{ACCENT_4} -")

    while True:
        password = getpass(f"{ACCENT_1} Password: {ACCENT_4}")
        confirm_password = getpass(f"{ACCENT_1} Confirm:  {ACCENT_4}")
        if confirm_password == 'x':
            quit()
        if len(password) < 8:
            template_red_messages("Make sure your password is at lest 8 letters".center(cols))
        elif len(password) > 64:
            template_red_messages("Maximální délka hesla - 64 Symbol".center(cols))
        elif password != confirm_password:
            template_red_messages("Passwords don't match".center(cols))
        elif re.search('[0-9]', password) is None:
            template_red_messages("Make sure your password has a number in it".center(cols))
        elif re.search('[a-z]', password) is None:
            template_red_messages("Make sure your password has lower case letters".center(cols))
        # elif re.search('[A-Z]', password) is None:
        #     template_red_messages("Make sure your password has upper case letters".center(cols))
        elif password == 'x':
            quit()
        elif password == confirm_password:
            return password
        else:
            template_red_messages("-_-".center(cols))


class ActionsWithPassword:
    """ Действия с пользовательскими паролями (в т.ч. мастер-паролем) """
    def __init__(self, type_password):
        self.type_pas = type_password

    def get_password(self):
        """ Получение паролей """

        def generation_new_password(length_password, add_random_symbols):
            """ Функция создания случайного пароля """
            symbols_for_password = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            additional_symbols = '!#$*()_-+[]{}?'
            if add_random_symbols:
                symbols_for_password += additional_symbols
            while True:
                if length_password >= 8:
                    new_password = ''
                    for i in range(length_password):
                        new_password += random.choice(symbols_for_password)
                    return new_password
                elif length_password < 8:
                    template_some_message(RED, ' The length must be at least 8 characters \n')
                    length_password = int(input(ACCENT_1 + ' - Length: ' + ACCENT_4))
                elif len(password) > 64:
                    template_red_messages("Maximální délka hesla - 64 Symbol".center(cols))

        # Создание мастер-пароля, создание хеша и сохранение в файл
        if self.type_pas == 'master':
            template_some_message(ACCENT_1, ' - Pick a master-password - \n')
            master_password = create_and_confirm_user_password()
            # Хэш сохраняется в файл
            if CHECK_FILE_WITH_HASH is False:
                if CHECK_FOLDER_FOR_RESOURCE is False:
                    hash_to_file = generate_password_hash(master_password)
                    with open(FILE_WITH_HASH, 'w') as hash_pas:
                        hash_pas.write(hash_to_file)
                        hash_pas.close()
                    return master_password
            elif CHECK_FOLDER_FOR_RESOURCE:
                if CHECK_FILE_WITH_HASH:
                    if CHECK_FILE_WITH_GENERIC:
                        return master_password

        # Сохранение пользовательского пароля для ресурсов
        elif self.type_pas == 'self':
            template_some_message(ACCENT_1, "- Pick a self password - \n")
            password = create_and_confirm_user_password()
            template_some_message(GREEN, "--- Your password success saved! ---")
            sleep(1)
            return password

        # Получение нового сгенерированного пароля
        elif self.type_pas == 'gen_new':
            length_new_pas = int(input(f"{ACCENT_1}- Length: {ACCENT_4}"))
            status_adding_characters = False
            request_for_adding_characters = input(
                f"{ACCENT_1}- Add additional symbols? (Default: no) (y/n): {ACCENT_4}"
            )
            if request_for_adding_characters == 'y':
                status_adding_characters = True
            password = generation_new_password(length_new_pas, status_adding_characters)
            print(
                f'{ACCENT_3}\n - Your new password - '
                f'{GREEN}{password}{ACCENT_3}'
                f' - success saved{ACCENT_4}'
            )
            sleep(3)
            return password

        # Получение общего ключа
        elif self.type_pas == 'generic':
            generic = generation_new_password(random.randrange(2**5, 2**6), False)
            hash_to_file = generate_password_hash(generic)
            hash_gen = open(FILE_WITH_HASH_GENERIC_KEY, 'w')
            hash_gen.write(hash_to_file)
            hash_gen.close()
            return generic

    @staticmethod
    def verify_master_password(show_logotype):
        """ Проверка мастер-пароля """
        def get_master_password():
            input_master_password = getpass(
                f"{ACCENT_1}\n\n   {standard_location('/LOGIN')}{ACCENT_4}"
            )
            if input_master_password == 'x':
                quit()
            elif input_master_password == 'r':
                system_action('restart')
            elif input_master_password == 'a':
                logo_obs.animation()
            return input_master_password

        cnt_left = 3
        while True:
            if show_logotype:   # Вывод версии и логотипа
                logo_obs.show_name_program()
                logo_obs.elba()
            master_password = get_master_password()
            # Проверка хэша пароля
            hash_password = check_password_hash(open(FILE_WITH_HASH).readline(), master_password)
            if (CHECK_FILE_WITH_HASH is False) or (CHECK_FILE_WITH_GENERIC is False):
                if CHECK_FOLDER_FOR_RESOURCE:
                    template_remove_folder(FOLDER_WITH_DATA)
                    quit()
            # Если нет подтверждения
            if hash_password is False:
                system_action('clear')
                print(RED, '\n'*3, "-----  Wrong password  -----".center(cols), '\n'*3, ACCENT_3)
                print(' '*16, f"Attempts left: {RED}{cnt_left}{ACCENT_4}".center(cols))
                cnt_left -= 1
                sleep(1)
                system_action('clear')
                if cnt_left <= 0:
                    system_action('clear')
                    template_some_message(RED, "---  Limit is exceeded  ---")
                    write_log('Someone tried to enter', 'ALERT')
                    sleep(1)
                    animation()
            # Если есть подтверждение
            else:
                if hash_password and CHECK_FOLDER_FOR_RESOURCE:
                    if CHECK_FILE_WITH_GENERIC:
                        xzibit = security_obs.dec_aes(FILE_WITH_GENERIC_KEY, master_password)
                        check_with_xzibit = check_password_hash(
                            open(FILE_WITH_HASH_GENERIC_KEY).readline(), xzibit
                        )
                        if check_with_xzibit:
                            return master_password
                        else:
                            template_remove_folder(FOLDER_WITH_DATA)
                            quit()
                    else:
                        template_remove_folder(FOLDER_WITH_DATA)
                        quit()


def choice_generation_or_save_self_password(resource, login, master_password):
    """ Выбор пароля: генерирование нового или сохранение пользовательского """
    proposed_options = [
        "Generation new password",
        "Save your password"
    ]

    print('\n')
    functions_obs.StylishLook().scrolling_and_numbering_content(proposed_options)
    print('\n')

    while True:
        change_type = int(input('Change (1/2): '))
        if change_type == 1:  # Генерирование пароля и сохранение в файл
            password = ActionsWithPassword('gen_new').get_password()
            security_obs.save_data_to_file(resource, login, password, master_password, 'resource')
            # Костыль для выхода из цикла
            return 0
        elif change_type == 2:  # Сохранение пользовательского пароля
            password = ActionsWithPassword('self').get_password()
            security_obs.save_data_to_file(resource, login, password, master_password, 'resource')
            return 0
        else:   # Если ошибка выбора
            print(f"{RED}\n  -- Error of change. Please, change again -- {ACCENT_4}")
            sleep(1)
        system_action('clear')
