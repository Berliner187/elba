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
import passwords_obs

from main import *

from multiprocessing import Process


__version__ = '0.10-02'


def control_bus(generic_key):
    """ Цикл с отображением сохраненных ресурсов и выбор действий """

    user_actions = input(standard_location('')).lower()   # Выбор действия
    try:
        if '-a' in user_actions:  # Добавление нового ресурса
            system_action('clear')
            write_log("Add resource", "RUN")
            resources_obs.add_new_resource(generic_key)
            functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
            write_log("Add resource", "QUIT")

        if '-x' in user_actions:  # Выход
            system_action('clear')
            template_some_message(ACCENT_3, '--- ELBA CLOSED ---')
            write_log("ELBA", "QUIT")
            quit()

        elif '-r' in user_actions:  # Перезапуск
            system_action('clear')
            write_log("Restart", "OK")
            system_action('restart')

        elif '-c' in user_actions:    # Смена мастер-пароля
            system_action('clear')
            write_log("Change password", "RUN")
            change_mp_obs.change_master_password()
            write_log("Change password", "QUIT")

        elif '-d' in user_actions:    # Удаление ресурса
            write_log("Remove object", "RUN")
            # Process(target=a, kwargs={'sleep_time': 0.7})
            remove_obs.Remove(generic_key, 'resource').remove_object()
            functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
            write_log("Remove object", "QUIT")

        elif '-n' in user_actions:    # Добавление заметок
            write_log("Notes", "RUN")
            functions_obs.ProgramFunctions(generic_key, 'note').get_category_label()
            notes_obs.notes(generic_key)
            write_log("Notes", "QUIT")

        elif '-f' in user_actions:    # Шифрование файлов
            functions_obs.ProgramFunctions(generic_key, 'encryption').get_category_label()
            change_action = template_input(standard_location('/ENCRYPTION') + ACCENT_4)
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

        elif '-u' in user_actions:    # Обновление программы
            system_action('clear')
            write_log("Update", "RUN")
            update_obs.update()
            functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
            write_log("Update", "OK")

        elif '-z' in user_actions:    # Удаление всех данных
            system_action('clear')
            template_some_message(ACCENT_3, 'Verify master password')
            passwords_obs.ActionsWithPassword(None).verify_master_password(False)
            template_some_message(RED, '- Are you sure you want to delete all data? -')
            confirm = template_question('Remove ALL data?')
            if confirm == 'y':
                template_remove_folder(FOLDER_WITH_DATA)
                system_action('clear')
                quit()
            functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()

        elif '-i' in user_actions:
            system_action("clear")
            write_log("Info", "RUN")
            info_obs.Information().get_info()
            write_log("Get info", "QUIT")
            control_bus(generic_key)

        elif '-l' in user_actions:    # Чтение файла с логами
            system_action("clear")
            functions_obs.StylishLook().topper('LOGS')
            log_data = open(FILE_LOG, 'r')
            reader_log = DictReader(log_data, delimiter=';')
            try:
                for line in reader_log:
                    print(
                        "{:s} -- {:19s} --- {:5s} -- {:50s}".format(
                            line[FIELDS_LOG_FILE[0]], line[FIELDS_LOG_FILE[1]],
                            line[FIELDS_LOG_FILE[2]], line[FIELDS_LOG_FILE[3]]
                        )
                    )
                write_log("Check logs", "OK")
            except KeyError as error:
                write_log(error, "FAIL")
            template_some_message(ACCENT_1, "- Press Enter to exit -")

        elif '-o' in user_actions:    # Откат к старой сохраненной версии
            if os.path.exists(OLD_ELBA):
                write_log("Try roll back", "RUN")
                rollback_obs.rollback()
                write_log("Roll back", "OK")
                system_action('restart')
            else:
                template_some_message(ACCENT_1, '- No versions saved -')

        elif '-s' in user_actions:    # Пользовательские настройки
            write_log('Settings', 'RUN')
            settings_obs.settings()
            functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()

        elif user_actions.isnumeric():  # Отображение сохраненных данных о ресурсе
            try:
                user_actions = int(user_actions)
                system_action('clear')
                functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()

                path_to_resource = FOLDER_WITH_RESOURCES + os.listdir(FOLDER_WITH_RESOURCES)[user_actions-1]
                template_print_decryption_data(
                    'Resource', f"{path_to_resource}/{FILE_RESOURCE}", generic_key)
                template_print_decryption_data(
                    'Login', f"{path_to_resource}/{FILE_LOGIN}", generic_key)
                template_print_decryption_data(
                    'Password', f"{path_to_resource}/{FILE_PASSWORD}", generic_key)
            except IndexError:
                pass
        else:
            functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
    except ValueError:  # Обработка ошибки
        functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
    control_bus(generic_key)
