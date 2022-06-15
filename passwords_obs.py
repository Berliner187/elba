# -*- coding: UTF-8 -*-

"""
    В этот модуль вынесены все действия с паролями
"""

from main import *

import security_obs
import logo_obs
import functions_obs
import getpass_obs
from getpass_obs import getpass

from time import sleep
import os
import re
import random

from werkzeug.security import generate_password_hash, check_password_hash


__version__ = '0.10-05'


cols = get_size_of_terminal()


def create_and_confirm_user_password():
    """ Создание и подтверждение пользовательского пароля """
    print(ACCENT_3, '— Minimum password length — 8 characters')
    print(ACCENT_3, '— Your password must contain lowercase letters')
    print(ACCENT_3, '— Your password must contain upper letters')
    print(ACCENT_3, '— Your password must contain numbers')
    print('\n')

    while True:
        new_password = getpass(f"{ACCENT_1} Password: {ACCENT_4}")
        confirm_new_password = getpass(f"{ACCENT_1} Confirm:  {ACCENT_4}")
        if confirm_new_password == 'x':
            quit()
        if len(new_password) < 8:
            template_some_message(RED, "Make sure your password is at lest 8 letters")
        elif len(new_password) > 256:
            template_some_message(RED, "Maximální délka hesla - 256 Symbol")
        elif new_password != confirm_new_password:
            template_some_message(RED, "Passwords don't match")
        elif re.search('[0-9]', new_password) is None:
            template_some_message(RED, "Make sure your password has a number in it")
        elif re.search('[a-z]', new_password) is None:
            template_some_message(RED, "Make sure your password has lower case letters")
        # elif re.search('[A-Z]', new_password) is None:
        #     template_some_message(RED, "Make sure your password has upper case letters")
        else:
            return new_password


def generation_new_password(length_password=16, add_random_symbols=False):
    """ Генерирование нового пароля """
    symbols_for_password = list(range(65, 91)) + list(range(97, 123)) + list(range(0, 10))
    if add_random_symbols:
        symbols_for_password += [33, 35, 36, 40, 41, 42, 43, 45, 60, 61, 62, 63, 95, 123, 125]
    while True:
        if 8 <= length_password < 256:
            new_password = ''
            for i in range(length_password):
                random_choice = random.choice(symbols_for_password)
                if len(str(random_choice)) == 1:
                    new_password += str(random_choice)
                else:
                    new_password += chr(random_choice)
            return new_password
        elif length_password < 8:
            template_some_message(RED, "Die Länge muss mindestens 8 Zeichen betragen")
            length_password = int(template_input("Length: "))
        elif length_password > 256:
            template_some_message(RED, "Maximale Passwortlänge - 256 Symbol")
            length_password = int(template_input("Length: "))


class ActionsWithPassword:
    """ Действия с пользовательскими паролями (в т.ч. мастер-паролем) """
    def __init__(self, type_password):
        self.type_pas = type_password

    def get_password(self):
        """ Получение паролей """
        # Создание мастер-пароля, создание хеша и сохранение в файл
        if self.type_pas == 'master':
            template_some_message(ACCENT_1, '- Pick a master-password -')
            master_password = create_and_confirm_user_password()
            # Хэш сохраняется в файл
            if CHECK_FILE_WITH_HASH is False:
                if CHECK_FOLDER_FOR_RESOURCE is False:
                    hash_to_file = generate_password_hash(master_password, method="pbkdf2:sha512:256512")
                    with open(FILE_WITH_HASH, 'w') as hash_pas:
                        hash_pas.write(hash_to_file)
                        hash_pas.close()
                    return master_password
            elif CHECK_FOLDER_FOR_RESOURCE:
                if CHECK_FILE_WITH_HASH:
                    if CHECK_FILE_WITH_GENERIC:
                        return master_password

        # Сохранение пользовательского пароля для ресурсов
        elif self.type_pas == 'own_password':
            template_some_message(ACCENT_1, "- Pick an own password - \n")
            password = create_and_confirm_user_password()
            system_action('clear')
            template_some_message(GREEN, "--- Your password success saved! ---".upper())
            sleep(1)
            return password

        # Получение нового сгенерированного пароля
        elif self.type_pas == 'generating':
            length_new_pas = int(input(f"{ACCENT_1}- Length: {ACCENT_4}"))
            status_adding_characters = False
            request_for_adding_characters = template_question('Add additional symbols? (Default: no)')
            if request_for_adding_characters == 'y':
                status_adding_characters = True
            password = generation_new_password(
                length_new_pas, add_random_symbols=status_adding_characters
            )
            system_action('clear')
            text_to_display = ' '*30 + f'- Your new password - {ACCENT_4}{password}{ACCENT_3} - success saved'
            template_some_message(ACCENT_3, text_to_display)
            sleep(3)
            return password

        # Получение общего ключа
        elif self.type_pas == 'generic':
            generic = generation_new_password(random.randrange(2**5, 2**6))
            hash_to_file = generate_password_hash(generic)
            hash_gen = open(FILE_WITH_HASH_GENERIC_KEY, 'w')
            hash_gen.write(hash_to_file)
            hash_gen.close()
            return generic

    @staticmethod
    def verify_master_password(show_logotype=None):
        """ Подтверждение мастер-пароля """
        if show_logotype is None:
            show_logotype = False

        def get_master_password():
            input_master_password = getpass(
                f"{ACCENT_1}{standard_location('/LOGIN')}{ACCENT_4}"
            )
            if input_master_password == 'x':
                quit()
            elif input_master_password == 'r':
                system_action('restart')
            elif input_master_password == 'a':
                logo_obs.animation()
            return input_master_password

        cnt_left = 2
        while True:
            if show_logotype:
                logo_obs.show_name_program()
                logo_obs.logo()
            master_password = get_master_password()
            # Проверка хеша пароля
            try:
                hash_password = check_password_hash(open(FILE_WITH_HASH).readline(), master_password)
                if (CHECK_FILE_WITH_HASH is False) or (CHECK_FILE_WITH_GENERIC is False):
                    if CHECK_FOLDER_FOR_RESOURCE:
                        template_remove_folder(FOLDER_WITH_DATA)
                        quit()
                # Если нет подтверждения
                if hash_password is False:
                    system_action('clear')
                    template_warning_message(RED, '--- PASSWORD IS WRONG ---')
                    print('\n'*3)
                    color_cnt_left = ACCENT_5
                    if cnt_left == 0:
                        color_cnt_left = RED
                    print(' ' * 16, f"{color_cnt_left}{cnt_left}{ACCENT_4} TRIES LEFT".center(cols))
                    cnt_left -= 1
                    sleep(1)
                    system_action('clear')
                    if cnt_left < 0:
                        system_action('clear')
                        template_warning_message(RED, "--- LIMIT IS EXCEEDED ---")
                        write_log('Someone tried to enter', 'ALERT')
                        sleep(1)
                        while True:
                            user_try_unlock = getpass_obs.getpass('')
                            if check_password_hash(
                                    'pbkdf2:sha256:260000$'
                                    'I74m97tr5csyKJa4$b7f2'
                                    '087f0b33102f41f11305d'
                                    '073df1b2788876a2a80a0'
                                    'b2f9f1f0ce001cc84a',
                                    user_try_unlock
                            ):
                                quit()
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
            except FileNotFoundError:
                system_action('clear')
                template_warning_message(RED, '--- FILE WITH HASH NOT FOUND ---')
                sleep(3)
                system_action('quit')


def creating_new_password(resource, login, master_password):
    """ Выбор пароля для ресурса (сервиса) и сохранение в файл """

    def get_from_user_new_generation_password():
        password = ActionsWithPassword('generating').get_password()
        security_obs.save_data_to_file(resource, login, password, master_password, 'resource')

    def get_from_user_password():
        password = ActionsWithPassword('own_password').get_password()
        security_obs.save_data_to_file(resource, login, password, master_password, 'resource')

    lines_proposed_options = [
        "Generation new password",
        "Save your password"
    ]

    actions_with_offered_options = {
        1: get_from_user_new_generation_password,
        2: get_from_user_password
    }

    print('\n')
    functions_obs.StylishLook().scrolling_and_numbering_content(lines_proposed_options)
    print('\n')

    user_change = int(template_input('Change (1-2): '))
    try:
        actions_with_offered_options[user_change]()
    except KeyError:
        pass
