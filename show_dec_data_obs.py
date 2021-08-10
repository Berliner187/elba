# -*- coding: UTF-8 -*-
from enc_obs import *


__version__ = '1.3.1'


cols = get_size_of_terminal()


def show_decryption_data(generic_key, category):
    """ Показ сохраненых ресурсов/заметок """
    system_action('clear')
    separator = '  '
    if category == 'note':
        separator += '  '

    lines_show_category = [
        BLUE,
        f"_______________________",
        f"                                     /\/| {YELLOW}\/           \/{BLUE} |\/\ ",
        f"                                    /\/\|{YELLOW}\/{separator}{category.upper()}S{separator}\/{BLUE}|/\/\ ",
        f"{YELLOW}                  \/               \/",
        '\n'
    ]
    for line_pic_category in lines_show_category:
        print(line_pic_category.center(cols))

    type_folder = ''
    if category == 'resource':
        type_folder = FOLDER_WITH_RESOURCES
    elif category == 'note':
        type_folder = FOLDER_WITH_NOTES

    number_saved_data = 0   # number_saved_data
    for category_item in os.listdir(type_folder):
        decryption_data = dec_only_base64(category_item, generic_key)
        number_saved_data += 1
        print(f"  {BLUE}{number_saved_data}. {YELLOW}{decryption_data}{DEFAULT_COLOR}")
    if number_saved_data == 0:
        print(f"{YELLOW}   No saved {category}s {DEFAULT_COLOR}")

    # <<< Показ инструкций, которые возможны для выполнения в данном окне >>>
    lines_instruction = []
    if category == 'resource':
        backup_message = ''
        if os.path.exists(OLD_ELBA):
            backup_message = f'{BLUE} - Enter \'-o\' to rollback'
        lines_instruction = [
            BLUE,
            ' - Enter \'-r\' to restart, \'-x\' to exit',
            ' - Enter \'-a\' to add new resource       ',
            ' - Enter \'-d\' to remove resource        ',
            ' - Enter \'-c\' to change master-password ',
            ' - Enter \'-n\' to go to notes            ',
            ' - Enter \'-f\' to encrypt your files     ',
            ' - Enter \'-s\' to go to settings         ',
            ' - Enter \'-u\' to update program         ',
            ' - Enter \'-z\' to remove ALL data        ',
            backup_message
        ]
    elif category == 'note':
        lines_instruction = [
            BLUE,
            '  - Press "Enter" to go back  ',
            '  - Enter "-a" to add new note',
            '  - Enter "-d" to remove note '
        ]

    for line_inst in lines_instruction:
        print(line_inst)
    print(f'\n{YELLOW} Select {category} by number \n', DEFAULT_COLOR)
