from main import *

from enc_obs import enc_aes, dec_aes
from actions_with_password_obs import create_and_confirm_user_password

from werkzeug.security import generate_password_hash, check_password_hash
from stdiomask import getpass

from time import sleep
import os


__version__ = '4.0.0'


def change_master_password():
    system_action('clear')

    def get_confirm_master_password():
        while True:
            _confirm_master_password = getpass(YELLOW + ' -- Enter your master-password: ' + DEFAULT_COLOR)
            open_file_with_hash = open(FILE_WITH_HASH).readline()
            check_master_password = check_password_hash(open_file_with_hash, _confirm_master_password)
            if check_master_password is False:
                print(RED + '\n --- Wrong master-password --- ' + DEFAULT_COLOR)
                sleep(1)
            else:
                return _confirm_master_password

    confirm_master_password = get_confirm_master_password()
    system_action('clear')
    print(GREEN + '\n\n  --  Success confirm  -- ' + DEFAULT_COLOR)
    sleep(.6)
    system_action('clear')
    print(BLUE + '\n   Pick a new master-password \n' + DEFAULT_COLOR)
    new_master_password = create_and_confirm_user_password()
    # Generic-key шифруется новым мастер-паролем
    generic_key_from_file = dec_aes(FILE_WITH_GENERIC_KEY, confirm_master_password)
    enc_aes(FILE_WITH_GENERIC_KEY, generic_key_from_file, new_master_password)

    new_hash = generate_password_hash(new_master_password)
    with open(FILE_WITH_HASH, 'w') as hash_pas:
        hash_pas.write(new_hash)
        hash_pas.close()

    system_action('clear')
    print(GREEN + '\n\n    -  Password changed successfully!  - ' + DEFAULT_COLOR)
    sleep(1)
    system_action('restart')
