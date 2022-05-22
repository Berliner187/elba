# -*- coding: UTF-8 -*-

"""
    Модуль, отвечающий за управление функциями программы.
    Тут можно подключать новые функции Эльбы.
    В этом модуле пользователь выбирает действия для выполнения,
    а control_bus (шина управления) передает управление другим модулям.
"""

import os

import resources_obs
import remove_obs
import functions_obs
import change_mp_obs
import notes_obs
import update_obs
import settings_obs
import info_obs
import rollback_obs
import security_obs

from main import *


__version__ = '0.10-01'


def control_bus(generic_key):
    """ Цикл с выводом сохраненных ресурсов и выбор действий """

    def drawing_instructions():
        functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()

    change_resource_or_actions = input(standard_location('')).lower()   # Выбор действия
    try:
        if '-a' in change_resource_or_actions:  # Добавление нового ресурса
            system_action('clear')
            resources_obs.add_new_resource(generic_key)
            drawing_instructions()
            write_log("Add resource", "QUIT")

        if '-x' in change_resource_or_actions:  # Выход
            system_action('clear')
            template_some_message(ACCENT_3, '--- ELBA CLOSED ---')
            write_log("ELBA", "CLOSE")
            quit()

        elif '-r' in change_resource_or_actions:  # Перезапуск
            system_action('clear')
            write_log("Restart", "OK")
            system_action('restart')

        elif '-c' in change_resource_or_actions:    # Смена мастер-пароля
            system_action('clear')
            change_mp_obs.change_master_password()
            write_log("Change password", "QUIT")

        elif '-d' in change_resource_or_actions:    # Удаление ресурса
            remove_obs.remove_object('resource')
            functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
            write_log("Remove object", "QUIT")

        elif '-n' in change_resource_or_actions:    # Добавление заметок
            functions_obs.ProgramFunctions(generic_key, 'note').get_category_label()
            notes_obs.notes(generic_key)
            write_log("Exit from notes", "QUIT")

        elif '-f' in change_resource_or_actions:    # Шифрование файлов
            functions_obs.ProgramFunctions(generic_key, 'encryption').get_category_label()
            change_action = input(ACCENT_4 + standard_location('/ENCRYPTION') + ACCENT_4)
            if '-e' in change_action:
                system_action('clear')
                system_action('file_manager')
                write_log("Try encryption", "RUN")
                security_obs.WorkWithUserFiles(generic_key, 'enc').file_encryption_control()
            elif '-d' in change_action:
                system_action('clear')
                write_log("Try decryption", "RUN")
                security_obs.WorkWithUserFiles(generic_key, 'dec').file_encryption_control()
            write_log("Exit from encrypt", "QUIT")
            functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()

        elif '-u' in change_resource_or_actions:    # Обновление программы
            system_action('clear')
            update_obs.update()
            functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
            write_log("Update", "OK")

        elif '-z' in change_resource_or_actions:    # Удаление всех данных
            system_action('clear')
            template_some_message(RED, ' - Are you sure you want to delete all data? - ')
            change_yes_or_no = input(ACCENT_1 + ' - Remove ALL data? (y/n): ' + ACCENT_4)
            if change_yes_or_no == 'y':
                template_remove_folder(FOLDER_WITH_DATA)
                system_action('clear')
                quit()
            drawing_instructions()

        elif '-i' in change_resource_or_actions:
            system_action("clear")
            info_obs.Information().get_info()
            write_log("Get info", "QUIT")
            control_bus(generic_key)

        elif '-l' in change_resource_or_actions:
            system_action("clear")
            functions_obs.StylishLook().topper('LOGS')
            log_data = open(FILE_LOG, 'r')
            reader_log = DictReader(log_data, delimiter=';')
            try:
                for line in reader_log:
                    print(
                        line[FIELDS_LOG_FILE[0]],
                        line[FIELDS_LOG_FILE[1]],
                        line[FIELDS_LOG_FILE[2]],
                        line[FIELDS_LOG_FILE[3]]
                    )
                write_log("Check logs", "QUIT")
            except KeyError as error:
                write_log(error, "FAILED")
            template_some_message(ACCENT_1, " - Press Enter to exit - ")

        elif '-o' in change_resource_or_actions:    # Откат к старой сохраненной версии
            if os.path.exists(OLD_ELBA) is False:
                template_some_message(ACCENT_1, '- No versions saved - ')
            else:
                write_log("Try roll back", "RUN")
                rollback_obs.rollback()
                write_log("Success roll back", "QUIT")
                system_action('restart')

        elif '-s' in change_resource_or_actions:    # Пользовательские настройки
            write_log('Settings', 'Run')
            settings_obs.settings()
            functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
            write_log('Settings', 'Exit')

        elif change_resource_or_actions.isnumeric():   # Вывод сохраненных данных о ресурсе
            match_string = 0
            for resource_in_folder in os.listdir(FOLDER_WITH_RESOURCES):
                match_string += 1
                if match_string == int(change_resource_or_actions):
                    system_action('clear')
                    drawing_instructions()

                    def template_print_decryption_data(data_type, value):
                        print(
                            ACCENT_3, data_type, ACCENT_4, security_obs.dec_aes(value, generic_key)
                        )

                    path_to_resource = FOLDER_WITH_RESOURCES + resource_in_folder
                    template_print_decryption_data(
                        'Resource --->', f"{path_to_resource}/{FILE_RESOURCE}")
                    template_print_decryption_data(
                        'Login ------>', f"{path_to_resource}/{FILE_LOGIN}")
                    template_print_decryption_data(
                        'Password --->', f"{path_to_resource}/{FILE_PASSWORD}")
            if match_string == 0:
                drawing_instructions()
        else:
            drawing_instructions()
    except ValueError:  # Обработка ошибки
        drawing_instructions()
    control_bus(generic_key)
