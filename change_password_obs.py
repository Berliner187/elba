from main import *

from csv import DictReader, DictWriter
from enc_obs import enc_aes, dec_aes, enc_only_base64, dec_only_base64
from datetime_obs import greeting

from werkzeug.security import generate_password_hash, check_password_hash
from stdiomask import getpass

from time import sleep
from shutil import copyfile
import os


__version__ = '2.0.0'


def change_master_password():
    system_action('clear')

    def user_input_password():
        print(BLUE + '\n Minimum password length 8 characters' + DEFAULT_COLOR)

        def input_password():
            password = getpass(YELLOW + 'Password: ' + DEFAULT_COLOR)
            confirm_pas = getpass(YELLOW + 'Confirm: ' + DEFAULT_COLOR)
            if confirm_pas == 'x':
                quit()
            return password, confirm_pas

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

    # Сверяются хеши паролей
    try:
        confirm_master_password = getpass(YELLOW + ' -- Enter your master-password: ' + DEFAULT_COLOR)
        open_file_with_hash = open(FILE_WITH_HASH).readline()
        check_master_password = check_password_hash(open_file_with_hash, confirm_master_password)

        if check_master_password == bool(False):
            print(RED + '\n --- Wrong password --- ' + DEFAULT_COLOR)
            sleep(1)
            decryption_block(None)
        else:
            system_action('clear')
            print(GREEN + '\n\n  --  Success confirm  -- ' + DEFAULT_COLOR)
            sleep(.6)
            system_action('clear')
            print(BLUE + '\n   Pick a new master-password \n' + DEFAULT_COLOR)
            new_master_password = user_input_password()

            mas_resources, mas_login, mas_password = [], [], []

            def path_to_resource(file_type):
                path = FOLDER_WITH_RESOURCES + resource_dir + '/' + file_type
                return path

            def template_append_data(file_type, massive, confirm_master_password):
                path = path_to_resource(file_type)
                dec_data = dec_aes(path, confirm_master_password)
                massive.append(dec_data)

            for resource_dir in os.listdir(FOLDER_WITH_RESOURCES):
                for resource_file in os.listdir(FOLDER_WITH_RESOURCES + resource_dir + '/'):

                    if resource_file == FILE_RESOURCE:
                        template_append_data(FILE_RESOURCE, mas_resources, confirm_master_password)

                    elif resource_file == FILE_LOGIN:
                        template_append_data(FILE_LOGIN, mas_login, confirm_master_password)

                    elif resource_file == FILE_PASSWORD:
                        template_append_data(FILE_PASSWORD, mas_password, confirm_master_password)

            for old_resource in os.listdir(FOLDER_WITH_RESOURCES):
                os.system("rm -r " + FOLDER_WITH_RESOURCES + old_resource)

            for i in range(len(mas_resources)):
                save_data_to_file(mas_resources[i], mas_login[i], mas_password[i], new_master_password)

            new_hash = generate_password_hash(new_master_password)
            with open(FILE_WITH_HASH, 'w') as hash_pas:
                hash_pas.write(new_hash)
                hash_pas.close()

        greeting(new_master_password, True)

        system_action('clear')
        print(GREEN + '\n\n    -  Password changed successfully!  - ' + DEFAULT_COLOR)
        sleep(1)
        system_action('restart')
    except TypeError:
        pass
