from main import *

import random
from time import sleep
import os

from werkzeug.security import generate_password_hash
from stdiomask import getpass


__version__ = '1.1.1'

# Символы, используемые для генерирования пароля
symbols_for_password = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-='


def create_and_confirm_user_password():
    print(BLUE + '\n Minimum password length 8 characters' + DEFAULT_COLOR)

    def input_password():
        password_from_user = getpass(YELLOW + 'Password: ' + DEFAULT_COLOR)
        confirm_password_from_user = getpass(YELLOW + 'Confirm: ' + DEFAULT_COLOR)
        if confirm_password_from_user == 'x':
            quit()
        return password_from_user, confirm_password_from_user

    user_password, user_confirm_password = input_password()

    if (user_password != user_confirm_password) or (len(user_password) or len(user_confirm_password)) < 8:
        print(RED + '\n Error of confirm. Try again \n' + DEFAULT_COLOR)

        # Условия принятия и подтверждения пароля
        password, confirm_pas = input_password()
        if (password == confirm_pas) and (len(password and confirm_pas) >= 8):
            return password
        else:
            print(RED + '\n Error in confirm \n' + DEFAULT_COLOR)
            while (password != confirm_pas) or (len(password or confirm_pas < 8)):
                password, confirm_pas = input_password()
                if (password == confirm_pas) and (len(password and confirm_pas) >= 8):
                    return password
                else:
                    print(RED + '\n Error in confirm \n' + DEFAULT_COLOR)

    elif (user_password == user_confirm_password) and (len(user_password) and len(user_confirm_password)) >= 8:
        return user_confirm_password


def actions_with_password(type_pas):
    """ Подтвержение пользовательского пароля """

    def generation_new_password():
        """ Функция создания случайного пароля """
        length_new_pas = int(input(YELLOW +
            ' - Length password (Minimum 8): ' +
             DEFAULT_COLOR))
        if length_new_pas > 8:
            new_password = ''
            for i in range(length_new_pas):
                new_password += random.choice(symbols_for_password)
            return new_password
        else:
            print(red + '\n Error of confirm. Try again \n' + DEFAULT_COLOR)
            generation_new_password()

    print(BLUE, '\n\n - Minimum Length password is 8 symbols', DEFAULT_COLOR)
    if type_pas == 'self':  # Собсвенный пароль для ресурса
        print(BLUE, ' - Pick a self password: ', DEFAULT_COLOR)
        password = create_and_confirm_user_password()
        print(BLUE + ' - Your password success saved' + DEFAULT_COLOR)
        sleep(1)
        return password

    elif type_pas == 'master':  # Мастер пароль
        print(BLUE + ' - Pick a master-password - \n')
        master_password = create_and_confirm_user_password()
        # Хэш сохраняется в файл
        if (CHECK_FILE_WITH_HASH is False) and (CHECK_FILE_WITH_HASH is False):
            """ Создание хэша пароля и запись его в файл """
            hash_to_file = generate_password_hash(master_password)
            with open(FILE_WITH_HASH, 'w') as hash_pas:
                hash_pas.write(hash_to_file)
                hash_pas.close()
            return master_password

        elif (CHECK_FILE_FOR_RESOURCE and CHECK_FILE_WITH_HASH) is True:
            return master_password

    elif type_pas == 'gen_new':     # Генерирование нового пароля
        password = generation_new_password()
        print(YELLOW + ' - Your new password - ',
              GREEN, password, YELLOW,
              ' - success saved', DEFAULT_COLOR)
        sleep(2)
        return password
