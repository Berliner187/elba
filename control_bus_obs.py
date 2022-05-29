# -*- coding: UTF-8 -*-

"""
    Модуль, отвечающий за управление функциями программы.
    Тут можно подключать новые функции Эльбы.
    В этом модуле пользователь выбирает действия для выполнения,
    а control_bus (шина управления) передает управление другим модулям и функциям.
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


__version__ = '0.10-03'


def control_bus(generic_key):
    """ Цикл с выводом сохраненных ресурсов и выбор действий """

    def add_resource():
        system_action('clear')
        write_log("Add resource", "RUN")
        resources_obs.add_new_resource(generic_key)
        functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
        write_log("Add resource", "QUIT")

    def close_program():
        system_action('clear')
        template_some_message(ACCENT_3, '--- ELBA CLOSED ---')
        write_log("ELBA", "QUIT")
        quit()

    def restart_program():
        system_action('clear')
        write_log("Restart", "OK")
        system_action('restart')

    def change_master_password():
        system_action('clear')
        write_log("Change password", "RUN")
        change_mp_obs.change_master_password()
        write_log("Change password", "QUIT")

    def remove_resource():
        write_log("Remove resource", "RUN")
        remove_obs.remove_object('resource')
        functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
        write_log("Remove resource", "QUIT")

    def go_notes():
        write_log("Notes", "RUN")
        functions_obs.ProgramFunctions(generic_key, 'note').get_category_label()
        notes_obs.notes(generic_key)
        write_log("Notes", "QUIT")

    def go_encryptions():
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

    def update_program():
        system_action('clear')
        write_log("Update", "RUN")
        update_obs.update()
        functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
        write_log("Update", "OK")

    def remove_all_data():
        system_action('clear')
        template_some_message(ACCENT_3, 'Verify master password')
        passwords_obs.ActionsWithPassword(None).verify_master_password(False)
        template_some_message(RED, ' - Are you sure you want to delete all data? - ')
        confirm = template_question('Remove ALL data?')
        if confirm == 'y':
            template_remove_folder(FOLDER_WITH_DATA)
            system_action('clear')
            quit()
        functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()

    def get_info():
        system_action("clear")
        write_log("Info", "RUN")
        info_obs.Information().get_info()
        write_log("Get info", "QUIT")
        control_bus(generic_key)

    def check_logs():
        system_action("clear")
        functions_obs.StylishLook().topper('LOGS')
        log_data = open(FILE_LOG, 'r')
        reader_log = DictReader(log_data, delimiter=';')
        try:
            for line in reader_log:
                print(
                    "{:s} -- {:19s} --- {:7s} -- {:50s}".format(
                        line[FIELDS_LOG_FILE[0]], line[FIELDS_LOG_FILE[1]],
                        line[FIELDS_LOG_FILE[3]], line[FIELDS_LOG_FILE[2]]
                    )
                )
            write_log("Check logs", "OK")
        except KeyError as error:
            write_log(error, "FAIL")
        template_some_message(ACCENT_1, " - Press Enter to exit - ")

    def rollback():
        if os.path.exists(OLD_ELBA) is False:
            template_some_message(ACCENT_1, '- No versions saved - ')
        else:
            write_log("Try roll back", "RUN")
            rollback_obs.rollback()
            write_log("Roll back", "OK")
            system_action('restart')

    def go_settings():
        write_log('Settings', 'Run')
        settings_obs.settings()
        functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
        write_log('Settings', 'QUIT')

    action_list = {
        '-a': add_resource,
        '-d': remove_resource,
        '-n': go_notes,
        '-f': go_encryptions,
        '-c': change_master_password,
        '-s': go_settings,
        '-u': update_program,
        '-o': rollback,
        '-i': get_info,
        '-l': check_logs,
        '-r': restart_program,
        '-x': close_program,
        '-z': remove_all_data
    }

    user_actions = input(standard_location('')).lower()   # Выбор действия
    if user_actions.isnumeric():  # Вывод сохраненных данных о ресурсе
        user_actions = int(user_actions)
        system_action('clear')
        functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()

        def template_print_decryption_data(data_type, value):
            print(
                " {:8s} {:s}---{:s} {:s}".format(
                    data_type, ACCENT_2, ACCENT_4,
                    security_obs.dec_aes(value, generic_key))
            )

        path_to_resource = FOLDER_WITH_RESOURCES + os.listdir(FOLDER_WITH_RESOURCES)[user_actions-1]
        template_print_decryption_data(
            'Resource', f"{path_to_resource}/{FILE_RESOURCE}")
        template_print_decryption_data(
            'Login', f"{path_to_resource}/{FILE_LOGIN}")
        template_print_decryption_data(
            'Password', f"{path_to_resource}/{FILE_PASSWORD}")
    else:
        functions_obs.ProgramFunctions(generic_key, 'resource').get_category_label()
    try:
        action_list[user_actions]()
    except KeyError:
        pass
    control_bus(generic_key)
# control_bus('mWAEczwdSlZGtOKtLHC41rRF2KBO8CeE4OH')
