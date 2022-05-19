# -*- coding: UTF-8 -*-

"""
    Модуль для вывода ресурсов и заметок с действиями,
    которые могут выполнятся пользователем в данном окне
"""
import random

from main import *

import security_obs


__version__ = '0.10-01'


cols = get_size_of_terminal()   # Получение масштаба терминала


class ProgramFunctions(object):
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

        type_folder = ''
        if self.category == 'resource':
            type_folder = FOLDER_WITH_RESOURCES
        elif self.category == 'note':
            type_folder = FOLDER_WITH_NOTES
        elif self.category == 'encryption':
            type_folder = FOLDER_WITH_ENC_DATA

        # <<< Показ категории >>>
        """ Топпер """
        location_above = f'ELBA/{self.category.upper()}S'

        def random_design(length):
            number_str = ''
            for i in range(length):
                number = random.randrange(0, 9)
                number_str += str(number)
            return number_str

        top_string = random_design(cols-1)
        middle_string = random_design(((cols - 1) - (len(location_above) + 4)))
        bottom_string = random_design(cols-1)

        print(ACCENT_2, "\n", top_string)               # 1 строка
        print(ACCENT_2, f"19{ACCENT_5} {location_above} {ACCENT_2}" + middle_string)  # 2 строка
        print(ACCENT_2, bottom_string, "\n"*2)          # 3 строка

        number_saved_data = 0
        for category_item in os.listdir(type_folder):
            if self.category != 'encryption':
                decryption_data = security_obs.dec_only_base64(category_item, self.generic)
            else:
                decryption_data = category_item
            number_saved_data += 1
            print(f" {ACCENT_3}[{ACCENT_1}{number_saved_data}{ACCENT_3}] {ACCENT_4}{decryption_data}")
        if number_saved_data == 0:
            print(f"{ACCENT_1}   No saved {self.category}s {ACCENT_4}")

        # <<< Показ инструкций, которые возможны для выполнения в данном окне >>>
        def template_show_functions(key, message):
            """ Шаблон инструкций для пользователя """
            return f"{ACCENT_3} [{ACCENT_1}{key}{ACCENT_3}]  —  {message}"

        # Для ресурсов:
        lines_instruction = []
        if self.category == 'resource':
            backup_message = ''
            if os.path.exists(OLD_ELBA):
                backup_message = template_show_functions('-O', 'Rollback')
            lines_instruction = [
                ACCENT_3,
                template_show_functions('-A', 'Add new resource'),
                template_show_functions('-D', 'Remove resource'),
                template_show_functions('-N', 'Go to notes'),
                template_show_functions('-F', 'Encrypt your files'),
                template_show_functions('-C', 'Change master-password'),
                template_show_functions('-S', 'Go to settings'),
                template_show_functions('-U', 'Update program'),
                backup_message,
                template_show_functions('-R', 'Restart'),
                template_show_functions('-X', 'Exit'),
                template_show_functions('-Z', 'Remove ALL data')
            ]

        # Для заметок:
        elif self.category == 'note':
            lines_instruction = [
                ACCENT_3,
                template_show_functions("-A", 'Add new note'),
                template_show_functions("-D", 'Remove note'),
                template_show_functions("Enter", 'Go back')
            ]

        # Для шифрованных файлов:
        elif self.category == 'encryption':
            template_some_message(ACCENT_3,
                                  f"-- Go to the {FOLDER_WITH_ENC_DATA} "
                                  f"data folder and follow the instructions below --")
            lines_instruction = [
                ACCENT_3,
                template_show_functions('-E', 'Encryption files'),
                template_show_functions('-D', 'Decryption files'),
                template_show_functions('Enter', 'Go back')
            ]

        for line_inst in lines_instruction:
            print(line_inst)

        if self.category != 'encryption':   # Исключения для лейбла заметок и ресурсов
            print(ACCENT_1, f'\n [ - Select {self.category} by number - ]\n'.upper(), ACCENT_4)
