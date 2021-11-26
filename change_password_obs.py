from main import *

from enc_obs import *
from actions_with_password_obs import create_and_confirm_user_password

from werkzeug.security import generate_password_hash, check_password_hash
from stdiomask import getpass

from time import sleep
import os


__version__ = '0.9-00'


def change_master_password():
    """ Смена мастер-пароля """

    def get_confirm_master_password():
        while True:
            system_action('clear')
            _confirm_master_password = getpass(ACCENT_1 + ' -- Enter your master-password: ' + ACCENT_4)
            open_file_with_hash = open(FILE_WITH_HASH).readline()
            check_master_password = check_password_hash(open_file_with_hash, _confirm_master_password)
            if check_master_password:
                return _confirm_master_password
            else:
                template_some_message(RED, ' --- Wrong master-password --- ')
                sleep(1)

    confirm_master_password = get_confirm_master_password()
    system_action('clear')
    template_some_message(GREEN, '  --  Success confirm  --')
    sleep(.6)
    system_action('clear')
    template_some_message(ACCENT_3, ' - Pick a new master-password -')
    new_master_password = create_and_confirm_user_password()
    # Generic-key шифруется новым мастер-паролем
    generic_key_from_file = dec_aes(FILE_WITH_GENERIC_KEY, confirm_master_password)
    enc_aes(FILE_WITH_GENERIC_KEY, generic_key_from_file, new_master_password)

    new_hash = generate_password_hash(new_master_password)
    with open(FILE_WITH_HASH, 'w') as hash_pas:
        hash_pas.write(new_hash)
        hash_pas.close()

    system_action('clear')
    template_some_message(GREEN, '-  Password changed successfully!  -')
    sleep(1)
    system_action('restart')
