# -*- coding: UTF-8 -*-

"""
    Модуль, отвечающий за управление функциями программы.
    API для взаимодействия пользователя с программой.
    В этом модуле пользователь выбирает дейсвия, необходимые для выполнения,
    а decryption_block передает управление другим модулям.
"""

import os

from del_object_obs import delete_object
from notes_obs import notes
from actions_with_password_obs import *
from category_actions_obs import CategoryActions
from update_obs import update, install_old_saved_version
from settings_obs import settings

import enc_obs

from main import *


__version__ = '0.9-02'


def decryption_block(generic_key):
    """ Цикл с выводом сохраненных ресурсов и выбор действий """
    change_resource_or_actions = input('\n ELBA: ~$ ')   # Выбор действия
    try:
        if change_resource_or_actions == '-a':  # Добавление нового ресурса
            system_action('clear')
            template_some_message(ACCENT_3, '--- Add new resource ---')
            resource = input(ACCENT_1 + ' Resource: ' + ACCENT_4)
            login = input(ACCENT_1 + ' Login: ' + ACCENT_4)
            choice_generation_or_save_self_password(resource, login, generic_key)
            write_log("Add resource", "QUIT")
            CategoryActions(generic_key, 'resource').get_category_label()

        elif change_resource_or_actions == '-u':    # Обновление программы
            system_action('clear')
            update()
            CategoryActions(generic_key, 'resource').get_category_label()
            write_log("Update", "OK")

        elif change_resource_or_actions == '-x':  # Выход
            system_action('clear')
            template_some_message(ACCENT_3, '--- ELBA CLOSED ---')
            write_log("Exit", "OK")
            quit()

        elif change_resource_or_actions == '-r':  # Перезапуск
            system_action('clear')
            write_log("Restart", "OK")
            system_action('restart')

        elif change_resource_or_actions == '-c':    # Смена мастер-пароля
            change_master_password()
            write_log("Change password", "QUIT")

        elif change_resource_or_actions == '-d':    # Удаление ресурса
            delete_object('resource')
            CategoryActions(generic_key, 'resource').get_category_label()
            write_log("Delete resource", "QUIT")

        elif change_resource_or_actions == '-n':    # Добавление заметок
            CategoryActions(generic_key, 'note').get_category_label()
            notes(generic_key)
            write_log("Exit from notes", "QUIT")

        elif change_resource_or_actions == '-f':    # Шифрование файлов
            CategoryActions(generic_key, 'encryption').get_category_label()
            change_action = input(ACCENT_1 + "\n - Select: " + ACCENT_4)
            if change_action == '-e':
                system_action('clear')
                system_action('file_manager')
                write_log("Try encryption", "RUN")
                enc_obs.WorkWithUserFiles(generic_key, 'enc').file_encryption_control()
            elif change_action == '-d':
                system_action('clear')
                write_log("Try decryption", "RUN")
                enc_obs.WorkWithUserFiles(generic_key, 'dec').file_encryption_control()
            write_log("Exit from encrypt", "QUIT")
            CategoryActions(generic_key, 'resource').get_category_label()

        elif change_resource_or_actions == '-z':    # Удаление всех данных
            system_action('clear')
            template_some_message(RED, ' - Are you sure you want to delete all data? - ')
            change_yes_or_no = input(ACCENT_1 + ' - Remove ALL data? (y/n): ' + ACCENT_4)
            if change_yes_or_no == 'y':
                template_remove_folder(FOLDER_WITH_DATA)
                system_action('clear')
                quit()

        elif change_resource_or_actions == '-i':
            system_action("clear")
            from information_obs import Information
            Information().get_info()
            write_log("Get info", "QUIT")
            decryption_block(generic_key)

        elif change_resource_or_actions == '-l':
            system_action("clear")
            template_some_message(GREEN, " Log program from file ")
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

        elif change_resource_or_actions == '-o':    # Откат к старой сохраненной версии
            if os.path.exists(OLD_ELBA) is False:
                template_some_message(ACCENT_1, '- No versions saved - ')
            else:
                write_log("Try roll back", "RUN")
                install_old_saved_version()
                write_log("Success roll back", "QUIT")
                system_action('restart')

        elif change_resource_or_actions == '-s':    # Пользовательские настройки
            settings(generic_key)

        elif change_resource_or_actions == '':  # Пасует ошибку
            CategoryActions(generic_key, 'resource').get_category_label()

        else:   # Вывод сохраненных данных о ресурсе
            s = 0
            for resource_in_folder in os.listdir(FOLDER_WITH_RESOURCES):
                s += 1
                if s == int(change_resource_or_actions):
                    system_action('clear')
                    CategoryActions(generic_key, 'resource').get_category_label()

                    path_to_resource = FOLDER_WITH_RESOURCES + resource_in_folder
                    resource_from_file = path_to_resource + '/' + FILE_RESOURCE
                    login_from_file = path_to_resource + '/' + FILE_LOGIN
                    password_from_file = path_to_resource + '/' + FILE_PASSWORD

                    def template_print_decryption_data(data_type, value):
                        print(ACCENT_3, data_type, ACCENT_1, enc_obs.dec_aes(value, generic_key), ACCENT_4)

                    template_print_decryption_data(
                        'Resource --->', resource_from_file)
                    template_print_decryption_data(
                        'Login ------>', login_from_file)
                    template_print_decryption_data(
                        'Password --->', password_from_file)

    except ValueError:  # Обработка ошибки
        CategoryActions(generic_key, 'resource').get_category_label()
    decryption_block(generic_key)
