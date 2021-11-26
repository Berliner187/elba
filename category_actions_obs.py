# -*- coding: UTF-8 -*-

"""
    Модуль для вывода ресурсов и заметок с действиями,
    которые могут выполнятся пользователем в данном окне
"""

from enc_obs import *
from main import *


__version__ = '0.9-01'


cols = get_size_of_terminal()   # Получение масштаба терминала


class CategoryActions(object):
    """
        1. Показ сохраненных ресурсов и действий в этой категории
        2. Показ сохраненных заметок и действий в этой категории
        3. Показ наименований папок, в которых были зашифрованы файлы,
        а также и действий в этой категории
    """

    def __init__(self, generic_key, category):
        self.generic = generic_key
        self.category = category

    def get_category_label(self):
        """ Вывод окна нужной категории """
        system_action('clear')
        separator = '  '

        type_folder = ''
        if self.category == 'resource':
            type_folder = FOLDER_WITH_RESOURCES
        elif self.category == 'note':
            separator *= 2
            type_folder = FOLDER_WITH_NOTES
        elif self.category == 'encryption':
            type_folder = FOLDER_WITH_ENC_DATA

        lines_show_category = [
            ACCENT_3,
            f"    _______________________\n"
            f"   /\/| {ACCENT_1}\/           \/{ACCENT_3} |\/\ \n"
            f"  /\/\|{ACCENT_1}\/{separator}{self.category.upper()}S{separator}\/{ACCENT_3}|/\/\ \n"
            f"  {ACCENT_1}    \/               \/",
            '\n'
        ]
        for line_pic_category in lines_show_category:
            print(line_pic_category.center(cols))

        number_saved_data = 0
        for category_item in os.listdir(type_folder):
            if self.category != 'encryption':
                decryption_data = dec_only_base64(category_item, self.generic)
            else:
                decryption_data = category_item
            number_saved_data += 1
            print(f"  {ACCENT_3}{number_saved_data}. {ACCENT_1}{decryption_data}{ACCENT_4}")
        if number_saved_data == 0:
            print(f"{ACCENT_1}   No saved {self.category}s {ACCENT_4}")

        # <<< Показ инструкций, которые возможны для выполнения в данном окне >>>
        # Для ресурсов:
        lines_instruction = []
        if self.category == 'resource':
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
        # Для заметок:
        elif self.category == 'note':
            lines_instruction = [
                ACCENT_3,
                '  - Press "Enter" to go back  ',
                '  - Enter \'-a\' to add new note',
                '  - Enter \'-d\' to remove note '
            ]
        # Для шифрованных файлов:
        elif self.category == 'encryption':
            system_action('clear')
            template_some_message(ACCENT_3,
                                  f"-- Go to the {FOLDER_WITH_ENC_DATA} data folder and follow the instructions --")
            lines_instruction = [
                ACCENT_3,
                ' - Press \'Enter\' to exit from encryption',
                ' - Enter \'-e\' to encryption files',
                ' - Enter \'-d\' to decryption files'
            ]

        for line_inst in lines_instruction:
            print(line_inst)
        print(f'\n{ACCENT_1} Select {self.category} by number \n', ACCENT_4)
