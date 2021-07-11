from main import *

from enc_obs import save_data_to_file
from logo_obs import elba

import random
from time import sleep
import os
import re

from werkzeug.security import generate_password_hash, check_password_hash
from stdiomask import getpass


__version__ = '2.0.0'


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


def point_of_entry():   # Точка входа в систему
    """ Получение мастер-пароля """
    def template_wrong_message(value_left):
        print(RED, '\n  ---  Wrong password --- ',
              BLUE, "\n\n Attempts left:",
              RED, value_left, DEFAULT_COLOR)
        sleep(1)

    def get_master_password():
        show_name_program()
        elba()
        user_master_password = getpass(
            YELLOW + '\n -- Your master-password: ' + DEFAULT_COLOR
        )
        if user_master_password == 'x':  # Досрочный выход из программы
            quit()
        elif user_master_password == 'r':
            system_action('restart')
        elif user_master_password == 'a':    # Показ анимации
            animation()
        elif user_master_password == 'n':
            author()
        elif user_master_password == 'u':
            from logo_obs import Ukraine
            Ukraine()
        return user_master_password

    master_password = get_master_password()

    # Удаление данных, если файл с хэшем не существует, но при этом есть сохраненные
    if os.path.exists(FILE_WITH_HASH) is False:
        if CHECK_FOLDER_FOR_RESOURCE is True:
            template_remove_folder(FOLDER_WITH_DATA)
            quit()

    # Проверка хэша пароля
    hash_pas_from_file = open(FILE_WITH_HASH, 'r')
    hash_password = check_password_hash(hash_pas_from_file.readline(), master_password)
    cnt_left = 3    # Счет оставшихся попыток

    if (hash_password and CHECK_FOLDER_FOR_RESOURCE) is False:    # Если хеши не совпадают
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
                write_log('Someone tried to enter', 'WARNING')
                sleep(2**10)
                quit()
            if hash_password:
                return master_password
            else:
                template_wrong_message(cnt_left)
    elif (hash_password and CHECK_FOLDER_FOR_RESOURCE) is True:
        return master_password
