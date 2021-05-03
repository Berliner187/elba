from main import *

import random
from time import sleep
import os

from werkzeug.security import generate_password_hash
from stdiomask import getpass


__version__ = '1.0.5'

# Символы, используемые для генерирования пароля
symbols_for_password = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-='


def confirm_user_password(type_pas):
    """ Подтвержение пользовательского пароля """

    def user_input_password():  # Подтверждение 
        print(BLUE + '\n Minimum password length 8 characters' + DEFAULT_COLOR)
        user_password = getpass('\n Password: ')
        if user_password == 'x':
            quit()
        user_confirm_password = getpass(' Confirm password: ')  # hide_password(' Confirm password: ')
        if user_password != user_confirm_password or len(user_password) < 8:
            print(RED + '\n Error of confirm. Try again \n' + DEFAULT_COLOR)
            quit()
        else:
            return user_password

    def generation_new_password():
        """ Функция создания случайного пароля """
        length_new_pas = int(input(YELLOW + ' - Length password (Minimum 8): ' + DEFAULT_COLOR))
        new_password = ''
        for pas_elem in range(length_new_pas):
            new_password += random.choice(symbols_for_password)
        if len(new_password) > 8:
            return new_password
        else:
            print(red + '\n Error of confirm. Try again \n' + DEFAULT_COLOR)
            generation_new_password()

    # Условаия принятия и подтверждения пароля
    if type_pas == 'self':  # Собсвенный пароль для ресурса
        password = user_input_password()
        print(BLUE + ' - Your password success saved' + DEFAULT_COLOR)
        sleep(1)
        return password
    elif type_pas == 'master':  # Мастер пароль
        master_password = user_input_password()
        # Хэш сохраняется в файл
        if (CHECK_FILE_WITH_HASH == bool(False)) and (CHECK_FILE_WITH_HASH == bool(False)):  # Создание хэша
            hash_to_file = generate_password_hash(master_password)
            with open(FILE_WITH_HASH, 'w') as hash_pas:
                hash_pas.write(hash_to_file)
                hash_pas.close()
            return master_password
        elif CHECK_FILE_FOR_RESOURCE and CHECK_FILE_WITH_HASH == bool(True):
            return master_password
    elif type_pas == 'gen_new':     # Генерирование нового пароля
        password = generation_new_password()
        print(YELLOW + ' - Your new password - ' + GREEN + password + DEFAULT_COLOR + ' - success saved' + DEFAULT_COLOR)
        sleep(2)
        return password


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
