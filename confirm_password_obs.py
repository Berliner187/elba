import random
from time import sleep
import os
# Сторонние модули (хэш пароля и скрытие ввода пароля)
from werkzeug.security import generate_password_hash
from stdiomask import getpass
# Импорт констант из главного файла
from main import yellow, blue, purple, green, red, mc
from main import file_hash_password, check_file_hash_password, check_file_date_base


__version__ = '1.0.4'

# List of all symbols for password
symbols_for_password = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-='


def confirm_user_password(type_pas, cnt=0):
    """ Подтвержение пользовательского пароля """
    def user_input_password():
        print(blue + '\n Minimum password length 8 characters' + mc)
        user_password = getpass('\n Password: ')
        if user_password == 'x':
            quit()
        user_confirm_password = getpass(' Confirm password: ')  # hide_password(' Confirm password: ')
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
