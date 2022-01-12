# -*- coding: UTF-8 -*-

"""
    Модуль для вывода ресурсов и заметок с действиями,
    которые могут выполнятся пользователем в данном окне
"""

from enc_obs import *
from main import *


__version__ = '0.9-04'


cols = get_size_of_terminal()   # Получение масштаба терминала


class CategoryActions(object):
    """
        1. Показ сохраненных ресурсов и действий в этой категории
        2. Показ сохраненных заметок и действий в этой категории
        3. Показ наименований папок, в которых были зашифрованы файлы,
        а также действий в этой категории
    """

    def __init__(self, generic_key, category):
        self.generic = generic_key
        self.category = category

    def get_category_label(self):
        """ Вывод окна нужной категории """
        system_action('clear')
        separator = "|"

        type_folder = ''
        if self.category == 'resource':
            type_folder = FOLDER_WITH_RESOURCES
            separator += "|"
        elif self.category == 'note':
            type_folder = FOLDER_WITH_NOTES
            separator += "|||"
        elif self.category == 'encryption':
            type_folder = FOLDER_WITH_ENC_DATA

        # <<< Показ категории >>>
        print(ACCENT_2, "\n", "|"*44)
        print(f" ||||||||||||{separator}{GREEN} ELBA/{self.category.upper()}S {ACCENT_2}{separator}||||||||||||")
        print(ACCENT_2, "|"*44, '\n'*2)

        number_saved_data = 0
        for category_item in os.listdir(type_folder):
            if self.category != 'encryption':
                decryption_data = dec_only_base64(category_item, self.generic)
            else:
                decryption_data = category_item
            number_saved_data += 1
            print(f" {ACCENT_3}[{ACCENT_1}{number_saved_data}{ACCENT_3}] {ACCENT_1}{decryption_data}{ACCENT_4}")
        if number_saved_data == 0:
            print(f"{ACCENT_1}   No saved {self.category}s {ACCENT_4}")

        # <<< Показ инструкций, которые возможны для выполнения в данном окне >>>
        def template_show_instructions(key, message):
            """ Шаблон инструкций для пользователя """
            user_input = "Enter"
            if key == 'Enter':
                user_input = "Press"
            return f"{ACCENT_3} |  {user_input} {ACCENT_1}{key}{ACCENT_3} to {message}"

        # Для ресурсов:
        lines_instruction = []
        if self.category == 'resource':
            backup_message = ''
            if os.path.exists(OLD_ELBA):
                backup_message = template_show_instructions('-O', 'rollback')
            lines_instruction = [
                ACCENT_3,
                template_show_instructions('-R', 'restart'),
                template_show_instructions('-X', 'exit'),
                template_show_instructions('-A', 'add new resource'),
                template_show_instructions('-D', 'remove resource'),
                template_show_instructions('-C', 'change master-password'),
                template_show_instructions('-N', 'go to notes'),
                template_show_instructions('-F', 'encrypt your files'),
                template_show_instructions('-S', 'go to settings'),
                template_show_instructions('-U', 'update program'),
                template_show_instructions('-Z', 'remove ALL data'),
                backup_message
            ]

        # Для заметок:
        elif self.category == 'note':
            lines_instruction = [
                ACCENT_3,
                template_show_instructions("Enter", 'go back'),
                template_show_instructions("-A", 'add new note'),
                template_show_instructions("-D", 'remove note')
            ]

        # Для шифрованных файлов:
        elif self.category == 'encryption':
            template_some_message(ACCENT_3,
                                  f"-- Go to the {FOLDER_WITH_ENC_DATA} data folder and follow the instructions --")
            lines_instruction = [
                ACCENT_3,
                template_show_instructions('Enter', 'exit from encryption'),
                template_show_instructions('-E', 'encryption files'),
                template_show_instructions('-D', 'decryption files')
            ]

        for line_inst in lines_instruction:
            print(line_inst)

        if self.category != 'encryption':   # Исключения для лейбла заметок и ресурсов
            print(ACCENT_1, f'\n [ - Select {self.category} by number - ]\n'.upper(), ACCENT_4)


# CategoryActions('xxx', 'encryption').get_category_label()
