from main import *

from enc_obs import *
from logo_obs import *

import random
from time import sleep
import os
import re

from werkzeug.security import generate_password_hash, check_password_hash
from stdiomask import getpass


__version__ = 'P8.6_M1.0'


cols = get_size_of_terminal()


def create_and_confirm_user_password():
    """ Создание и подтверждение пользовательского пароля """
    print(ACCENT_3, 'Minimum password length — 8 characters'.center(cols))

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
        elif password != confirm_password:
            template_red_messages("Passwords don't match".center(cols))
        elif re.search('[0-9]', password) is None:
            template_red_messages("Make sure your password has a number in it".center(cols))
        elif password == 'x':
            quit()
        else:
            return password


class ActionsWithPassword:
    """ Действия с пользовательскими паролями (в т.ч. мастер-паролем) """
    def __init__(self, type_password):
        self.type_pas = type_password

    def get_password(self):
        """ Получение паролей """

        def generation_new_password(length_password, add_random_symbols):
            """ Функция создания случайного пароля """
            symbols_for_password = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            additional_symbols = '!@#$%^&*()_-+[]{}№;:?'
            if add_random_symbols:
                symbols_for_password += additional_symbols
            while True:
                if length_password >= 8:
                    new_password = ''
                    for i in range(length_password):
                        new_password += random.choice(symbols_for_password)
                    return new_password
                else:
                    template_some_message(RED, ' The length must be at least 8 characters \n')
                    length_password = int(input(ACCENT_1 + ' - Length: ' + ACCENT_4))

        # Создание мастер-пароля, создание хеша и сохранение в файл
        if self.type_pas == 'master':
            template_some_message(ACCENT_3, ' - Pick a master-password - \n')
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
            template_some_message(ACCENT_3, "- Pick a self password - \n")
            password = create_and_confirm_user_password()
            template_some_message(GREEN, "--- Your password success saved! ---")
            sleep(1)
            return password

        # Получение нового сгенерированного пароля
        elif self.type_pas == 'gen_new':
            length_new_pas = int(input(f"{ACCENT_1}- Length: {ACCENT_4}"))
            status_adding_characters = False
            request_for_adding_characters = input(
                f"{ACCENT_3} - Add additional symbols? (Default: no) (y/n): {ACCENT_4}"
            )
            if request_for_adding_characters == 'y':
                status_adding_characters = True
            password = generation_new_password(length_new_pas, status_adding_characters)
            print(
                f'{ACCENT_3}\n - Your new password - {GREEN}{password}{ACCENT_3} - success saved{ACCENT_4}'
            )
            sleep(3)
            return password
        # Получение общего ключа
        elif self.type_pas == 'generic':
            generic = generation_new_password(32, False)
            hash_to_file = generate_password_hash(generic)
            hash_gen = open(FILE_WITH_HASH_GENERIC_KEY, 'w')
            hash_gen.write(hash_to_file)
            hash_gen.close()
            return generic


def choice_generation_or_save_self_password(resource, login, master_password):
    """ Выбор пароля: генерирование нового или сохранение пользовательского """
    print('\n'*2,
          f"{ACCENT_3}1.{ACCENT_1} - Generation new password \n",
          f"{ACCENT_3}2.{ACCENT_1} - Save your password      \n")
    print(ACCENT_4)
    change_type = int(input('Change (1/2): '))
    if change_type == 1:  # Генерирование пароля и сохранение в файл
        password = ActionsWithPassword('gen_new').get_password()
        save_data_to_file(resource, login, password, master_password, 'resource')
    elif change_type == 2:  # Сохранение пользовательского пароля
        password = ActionsWithPassword('self').get_password()
        save_data_to_file(resource, login, password, master_password, 'resource')
    else:   # Если ошибка выбора
        print(f"{RED}\n  -- Error of change. Please, change again -- {ACCENT_4}")
        sleep(1)
        system_action('clear')
        choice_generation_or_save_self_password(resource, login, master_password)
    system_action('clear')


def point_of_entry():   # Точка входа в систему
    """ Получение мастер-пароля """
    def template_wrong_message(value_left):
        system_action('clear')
        lines = [
            "\n\n\n",
            RED,
            "-----  Wrong password  -----",
            "\n\n\n",
            ACCENT_3,
            f"Attempts left: {RED}{value_left}",
            ACCENT_4
        ]
        wait_effect(lines, 0)
        sleep(1)

    def get_master_password():
        show_name_program()
        elba()
        input_master_password = getpass(
            f"{ACCENT_1}\n\n   --- Enter the master password: {ACCENT_4}"
        )
        if input_master_password == 'x':  # Досрочный выход из программы
            quit()
        elif input_master_password == 'r':
            system_action('restart')
        elif input_master_password == 'a':    # Показ анимации
            animation()
        elif input_master_password == 'n':   # Показ ника автора
            author()
        elif input_master_password == 'u':   # Слава Україні
            from logo_obs import Ukraine
            Ukraine()
        return input_master_password

    master_password = get_master_password()
    if (CHECK_FILE_WITH_HASH is False) or (CHECK_FILE_WITH_GENERIC is False):
        if CHECK_FOLDER_FOR_RESOURCE:
            template_remove_folder(FOLDER_WITH_DATA)
            quit()

    # Проверка хэша пароля
    hash_pas_from_file = open(FILE_WITH_HASH)
    hash_password = check_password_hash(hash_pas_from_file.readline(), master_password)
    cnt_left = 4
    if (hash_password and CHECK_FOLDER_FOR_RESOURCE) is False:
        cnt_left -= 1
        template_wrong_message(cnt_left)
        while hash_password is False:
            cnt_left -= 1
            system_action('clear')
            master_password = get_master_password()
            file_hash = open(FILE_WITH_HASH)
            hash_password = check_password_hash(file_hash.readline(), master_password)
            if cnt_left <= 0:
                system_action('clear')
                template_some_message(RED, "  ---  Limit is exceeded  --- ")
                write_log('Someone tried to enter', 'ALERT')
                sleep(2)
                animation()
                quit()
            if hash_password:
                return master_password
            else:
                template_wrong_message(cnt_left)
    elif hash_password and CHECK_FOLDER_FOR_RESOURCE:
        xzibit_from_file = open(FILE_WITH_HASH_GENERIC_KEY)
        xzibit = dec_aes(FILE_WITH_GENERIC_KEY, master_password)
        check_with_exibit = check_password_hash(xzibit_from_file.readline(), xzibit)
        if check_with_exibit is False:
            template_remove_folder(FOLDER_WITH_DATA)
            quit()
        else:
            return master_password
    else:
        quit()
