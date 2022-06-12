# -*- coding: UTF-8 -*-

"""
    Модуль для вывода ресурсов и заметок с действиями,
    которые могут выполнятся пользователем в данном окне
"""

from main import *
import random
import security_obs
import shutil


__version__ = '0.10-03'


cols = get_size_of_terminal()   # Получение масштаба терминала


class StylishLook:
    """ Стандартизация стиля в программе """
    @staticmethod
    def topper(category_display):
        """ Отображение топпера сверху """
        location_above = f'ELBA/{category_display.upper()}'

        def topper(topper_string):
            print(ACCENT_2, topper_string)

        def filling(length):
            number_str = ''
            for i in range(length):
                char = random.randrange(65, 91)
                number_str += chr(char)
            return number_str

        hollow_filled_string = filling(cols - 1)
        middle_string = filling(((cols - 1) - (len(location_above) + 4)))

        topper(hollow_filled_string)                                         # 1 строка
        topper(f"19 {ACCENT_5}{location_above}{ACCENT_2} " + middle_string)  # 2 строка
        topper(hollow_filled_string)                                         # 3 строка
        print(ACCENT_4, "\n" * 2)

    @staticmethod
    def scrolling_and_numbering_content(what_scrolls):
        cnt = 0
        for content in what_scrolls:
            cnt += 1
            print(f" {ACCENT_3}[{ACCENT_1}{cnt}{ACCENT_3}] - {content}{ACCENT_4}")
        return cnt


class ProgramFunctions(object):
    """
        Вывод инструкций к выбранной категории
        1. Отображение сохраненных сервисов и действий в этой категории
        2. Отображение сохраненных заметок и действий в этой категории
        3. Отображение наименований директорий, в которых были зашифрованы файлы,
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

        StylishLook().topper(self.category + 'S')

        # Прокрутка сохраненных данных
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

        # <<< Отображение инструкций, которые возможны для выполнения в данном окне >>>
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
                template_show_functions('-A', 'Add New Resource'),
                template_show_functions('-D', 'Remove Resource'),
                template_show_functions('-C', 'Change Master-Password'),
                template_show_functions('-F', 'File Encryption'),
                template_show_functions('-N', 'Notes'),
                template_show_functions('-S', 'Settings'),
                template_show_functions('-U', 'Update'),
                backup_message,
                template_show_functions('-R', 'Restart'),
                template_show_functions('-X', 'Exit'),
                template_show_functions('-Z', 'Remove ALL Data')
            ]

        # Для заметок:
        elif self.category == 'note':
            lines_instruction = [
                ACCENT_3,
                template_show_functions("-A", 'Add New Note'),
                template_show_functions("-D", 'Remove Note'),
                template_show_functions("Enter", 'Go back')
            ]

        # Для файлов, которые были зашифрованы/дешифрованы:
        elif self.category == 'encryption':
            template_some_message(ACCENT_3,
                                  "-- Go to the " + ACCENT_1 + FOLDER_WITH_ENC_DATA + ACCENT_3 +
                                  " data folder and follow the instructions below --")
            lines_instruction = [
                ACCENT_3,
                template_show_functions('-E', 'Encrypt File'),
                template_show_functions('-D', 'Decrypt File'),
                template_show_functions('Enter', 'Go back')
            ]

        for line_inst in lines_instruction:
            print(line_inst)

        if self.category != 'encryption':   # Исключения для лейбла заметок и ресурсов
            print(ACCENT_1, f'\n [ - Select {self.category} by number - ]\n'.upper(), ACCENT_4)
