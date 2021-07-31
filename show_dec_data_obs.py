# -*- coding: UTF-8 -*-
from enc_obs import *


__version__ = '1.2.6'


cols = get_size_of_terminal()


def show_decryption_data(generic_key, category):
    """ Показ сохраненых ресурсов/заметок """
    system_action('clear')
    separator = ''
    if category == 'note':
        separator += '    '

    lines_show_category = [
        f"{BLUE}   ___________________________________",
        f"{BLUE}              /\/| {YELLOW}\/                       \/{BLUE} |\/\ ",
        f"{BLUE}             /\/\| {YELLOW}\/    Saved {category}s {separator}   \/ {BLUE}|/\/\ ",
        f"{YELLOW}     \/                       \/ \n\n"
    ]
    for line_pic_category in lines_show_category:
        print(line_pic_category.center(cols))

    type_folder = ''
    if category == 'resource':
        type_folder = FOLDER_WITH_RESOURCES
    elif category == 'note':
        type_folder = FOLDER_WITH_NOTES

    s = 0   # number_saved_data
    for category_item in os.listdir(type_folder):
        decryption_data = dec_only_base64(category_item, generic_key)
        s += 1
        print(f"{BLUE}{s}. {YELLOW}{decryption_data}{DEFAULT_COLOR}")
    if s == 0:
        print(f"{YELLOW}   No saved {category}s {DEFAULT_COLOR}")
    if category == 'resource':
        backup_message = ''
        if os.path.exists(OLD_ELBA):
            backup_message = BLUE + '\n  - Enter \'-o\' to rollback'
        print(BLUE,
              '\n  - Enter \'-r\' to restart, \'-x\' to exit',
              '\n  - Enter \'-a\' to add new resource       ',
              '\n  - Enter \'-d\' to remove resource        ',
              '\n  - Enter \'-c\' to change master-password ',
              '\n  - Enter \'-n\' to go to notes            ',
              '\n  - Enter \'-f\' to encrypt your files     ',
              '\n  - Enter \'-u\' to update program         ',
              '\n  - Enter \'-z\' to remove ALL data        ',
              backup_message, YELLOW,
              '\n\n Select resource by number \n', DEFAULT_COLOR)
    elif category == 'note':
        lines_note_inst = [
            BLUE,
            '  - Press "Enter" to go back    ',
            '  - Enter "-a" to add new note  ',
            f'  - Enter "-d" to remove note{YELLOW}',
            f'\n Select note by number \n {DEFAULT_COLOR}'
        ]
        for line_inst in lines_note_inst:
            print(line_inst)
