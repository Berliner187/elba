from main import *
from enc_obs import save_data_to_file

from csv import DictReader, DictWriter
from enc_obs import enc_aes, dec_aes, enc_only_base64, dec_only_base64
from datetime_obs import greeting
from actions_with_password_obs import create_and_confirm_user_password

from werkzeug.security import generate_password_hash, check_password_hash
from stdiomask import getpass

from time import sleep
from shutil import copyfile
import os


__version__ = '2.0.2'


def change_master_password():
    system_action('clear')

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
            new_master_password = create_and_confirm_user_password()

            mas_resources, mas_login, mas_password = [], [], []

            def path_to_resource(file_type):
                path = FOLDER_WITH_RESOURCES + resource_dir + '/' + file_type
                return path

            def template_append_data(file_type, massive, confirmed_master_password):
                path = path_to_resource(file_type)
                dec_data = dec_aes(path, confirmed_master_password)
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
