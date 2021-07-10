from main import *

from enc_obs import save_data_to_file

import random
from time import sleep
import os
import re

from werkzeug.security import generate_password_hash
from stdiomask import getpass


__version__ = '1.2.0'


def create_and_confirm_user_password():
    """ Создание и подтверждение пользовательского пароля """
    print(BLUE + '\n Minimum password length — 8 characters' + DEFAULT_COLOR)

    def template_red_messages(message):
        system_action('clear')
        print(RED + '\n'*2 + ' - ' + message + DEFAULT_COLOR)

    while True:
        password = getpass(YELLOW + " Password: " + DEFAULT_COLOR)
        confirm_password = getpass(YELLOW + " Confirm:  " + DEFAULT_COLOR)
        if confirm_password == 'x':  quit()
        if len(password) < 8:
            template_red_messages("Make sure your password is at lest 8 letters")
        elif password != confirm_password:
            template_red_messages("Passwords don't match")
        elif re.search('[0-9]', password) is None:
            template_red_messages("Make sure your password has a number in it")
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
                symbols_for_password = symbols_for_password + additional_symbols
            if length_password > 8:
                new_password = ''
                for i in range(length_password):
                    new_password += random.choice(symbols_for_password)
                return new_password
            else:
                print(RED + '\n Error of confirm. Try again \n' + DEFAULT_COLOR)
                generation_new_password(length_password, add_random_symbols)

        # Получение собственного пароля для ресурсов
        if self.type_pas == 'self':
            print(BLUE, ' - Pick a self password: ', DEFAULT_COLOR)
            password = create_and_confirm_user_password()
            print(BLUE + ' - Your password success saved' + DEFAULT_COLOR)
            sleep(1)
            return password

        # Создание мастер-пароля, создание хеша и сохранение в файл
        elif self.type_pas == 'master':
            print(BLUE + ' - Pick a master-password - \n')
            master_password = create_and_confirm_user_password()
            # Хэш сохраняется в файл
            if (CHECK_FILE_WITH_HASH and CHECK_FILE_WITH_HASH) is False:
                hash_to_file = generate_password_hash(master_password)
                with open(FILE_WITH_HASH, 'w') as hash_pas:
                    hash_pas.write(hash_to_file)
                    hash_pas.close()
                return master_password

            elif (CHECK_FOLDER_FOR_RESOURCE and CHECK_FILE_WITH_HASH) is True:
                return master_password

        # Получение нового сгенерированного пароля
        elif self.type_pas == 'gen_new':
            length_new_pas = int(input(YELLOW + ' - Length: ' + DEFAULT_COLOR))
            request_for_adding_characters = input(
                BLUE + ' - Add additional symbols? (Default: no) (y/n): ' + DEFAULT_COLOR
            )
            if request_for_adding_characters == 'y':
                password = generation_new_password(length_new_pas, True)
            else:
                password = generation_new_password(length_new_pas, False)
            print(
                YELLOW, ' - Your new password -', GREEN, password,
                YELLOW, '- success saved', DEFAULT_COLOR
            )
            sleep(2)
            return password
        # Получение общего ключа
        elif self.type_pas == 'generic':
            generic = generation_new_password(32, False)
            return generic


def choice_generation_or_save_self_password(resource, login, master_password):
    """ Выбор пароля: генерирование нового или сохранение пользовательского """
    print('\n',
          GREEN + ' 1' + YELLOW + ' - Generation new password \n',
          GREEN + ' 2' + YELLOW + ' - Save your password      \n', DEFAULT_COLOR
          )
    change_type = int(input('Change (1/2): '))
    if change_type == 1:  # Генерирование пароля и сохранение в файл
        password = ActionsWithPassword('gen_new').get_password()
        save_data_to_file(resource, login, password, master_password, 'resource')
    elif change_type == 2:  # Сохранение пользовательского пароля
        password = ActionsWithPassword('self').get_password()
        save_data_to_file(resource, login, password, master_password, 'resource')
    else:   # Если ошибка выбора
        print(RED + '  -- Error of change. Please, change again --  ' + DEFAULT_COLOR)
        choice_generation_or_save_self_password(resource, login, master_password)
    system_action('clear')
