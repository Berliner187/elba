# -*- coding: UTF-8 -*-

"""
    Модуль для вывода ресурсов и заметок с действиями,
    которые могут выполнятся пользователем в данном окне
"""

from enc_obs import *


__version__ = 'P8.6_M1.0'

cols = get_size_of_terminal()


def show_decryption_data(generic_key, category):
    """ Показ сохраненых ресурсов/заметок """
    system_action('clear')
    separator = '  '
    if category == 'note':
        separator += '  '

    lines_show_category = [
        ACCENT_3,
        f"_______________________",
        f"                                     /\/| {ACCENT_1}\/           \/{ACCENT_3} |\/\ ",
        f"                                    /\/\|{ACCENT_1}\/{separator}{category.upper()}S{separator}\/{ACCENT_3}|/\/\ ",
        f"{ACCENT_1}                  \/               \/",
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
        print(f"  {ACCENT_3}{number_saved_data}. {ACCENT_1}{decryption_data}{ACCENT_4}")
    if number_saved_data == 0:
        print(f"{ACCENT_1}   No saved {category}s {ACCENT_4}")

    # <<< Показ инструкций, которые возможны для выполнения в данном окне >>>
    lines_instruction = []
    if category == 'resource':
        backup_message = ''
        if os.path.exists(OLD_ELBA):
            backup_message = f'{ACCENT_3} - Enter \'-o\' to rollback'
        lines_instruction = [
            ACCENT_3,
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
            ACCENT_3,
            '  - Press "Enter" to go back  ',
            '  - Enter "-a" to add new note',
            '  - Enter "-d" to remove note '
        ]

    for line_inst in lines_instruction:
        print(line_inst)
    print(f'\n{ACCENT_1} Select {category} by number \n', ACCENT_4)
