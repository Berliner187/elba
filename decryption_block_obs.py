# -*- coding: UTF-8 -*-
# Локальные модули
from logo_obs import elba, first_start_message
from datetime_obs import greeting
from del_object_obs import delete_resource
from notes_obs import notes
from change_password_obs import change_master_password
from actions_with_password_obs import choice_generation_or_save_self_password
from enc_obs import enc_aes, dec_aes, WorkWithUserFiles
from show_dec_data_obs import show_decryption_data
from update_obs import update, install_old_saved_version
from main import *


__version__ = '2.1.2'


def decryption_block(generic_key):
    """ Цикл с выводом сохраненных ресурсов """
    change_resource_or_actions = input('\n Change action: ')   # Выбор действия
    try:
        if change_resource_or_actions == '-a':  # Добавление нового ресурса
            system_action('clear')
            template_some_message(GREEN, '\n   --- Add new resource ---   \n\n\n')
            resource = input(YELLOW + ' Resource: ' + DEFAULT_COLOR)
            login = input(YELLOW + ' Login: ' + DEFAULT_COLOR)
            choice_generation_or_save_self_password(resource, login, generic_key)
            write_log("Add resource", "OK")
            show_decryption_data(generic_key, 'resource')

        elif change_resource_or_actions == '-u':    # Обновление программы
            system_action('clear')
            update()
            show_decryption_data(generic_key, 'resource')
            write_log("Update", "OK")

        elif change_resource_or_actions == '-x':  # Выход
            system_action('clear')
            template_some_message(BLUE, ' --- Program is closet --- \n')
            write_log("Exit", "OK")
            quit()

        elif change_resource_or_actions == '-r':  # Перезапуск
            system_action('clear')
            template_some_message(GREEN, ' --- Restart --- \n')
            sleep(.2)
            write_log("Restart", "OK")
            system_action('restart')

        elif change_resource_or_actions == '-c':    # Смена мастер-пароля
            change_master_password()
            write_log("Change password", "OK")

        elif change_resource_or_actions == '-d':    # Удаление ресурса
            delete_resource('resource')
            show_decryption_data(generic_key, 'resource')
            write_log("Delete resource", "OK")

        elif change_resource_or_actions == '-n':    # Добавление заметок
            show_decryption_data(generic_key, 'note')
            notes(generic_key)
            write_log("Go to notes", "OK")

        elif change_resource_or_actions == '-f':    # Шифрование файлов
            # Переписать под show_dec_data_obs
            system_action('clear')
            template_some_message(BLUE,
                                  "-- Go to the VOLARE/ENCRYPTION_DATA data folder and follow the instructions --")
            print(BLUE, "1.", YELLOW, " - Encryption files", DEFAULT_COLOR)
            print(BLUE, "2.", YELLOW, " - Decryption files", DEFAULT_COLOR)
            change_action = input(YELLOW + "\n - Select by number: " + DEFAULT_COLOR)
            if change_action == '1':
                system_action('clear')
                # system_action('file_manager')
                WorkWithUserFiles(generic_key, 'enc').file_encryption_control()
            elif change_action == '2':
                system_action('clear')
                WorkWithUserFiles(generic_key, 'dec').file_encryption_control()
            write_log("Encryption data", "OK")
            show_decryption_data(generic_key, 'resource')

        elif change_resource_or_actions == '-z':    # Удаление всех данных
            system_action('clear')
            template_some_message(RED, ' - Are you sure you want to delete all data? - ')
            change_yes_or_no = input(YELLOW + ' - Remove ALL data? (y/n): ' + DEFAULT_COLOR)
            if change_yes_or_no == 'y':
                template_remove_folder(FOLDER_WITH_DATA)
                system_action('clear')
                quit()

        elif change_resource_or_actions == '-s':
            from get_size_obs import size_all, get_versions
            get_versions()
            size_all()
            write_log("Get size and versions", "OK")
            decryption_block(generic_key)

        elif change_resource_or_actions == '-l':
            system_action("clear")
            template_some_message(GREEN, "\n Log program from file \n")
            log_data = open(FILE_LOG, 'r')
            reader_log = DictReader(log_data, delimiter=';')
            try:
                write_log("Check logs", "OK")
                for line in reader_log:
                    print(
                        line[FIELDS_LOG_FILE[0]],
                        line[FIELDS_LOG_FILE[1]],
                        line[FIELDS_LOG_FILE[2]],
                        line[FIELDS_LOG_FILE[3]]
                    )
            except KeyError:
                write_log("Check logs: KEY ERROR", "FAILED")
            template_some_message(YELLOW, " - Press Enter to exit - ")

        elif change_resource_or_actions == '-dm':  # Удаление кэша
            template_remove_folder('rm -r __pycache__/')
            system_action('clear')
            template_some_message(GREEN, " Success delete cache")
            write_log("Delete cache", "OK")
            sleep(1)
            system_action('restart')

        elif change_resource_or_actions == '-o':    # Откат к старой сохраненной версии
            if os.path.exists(OLD_ELBA) is False:
                template_some_message(YELLOW, ' - No versions saved - ')
            else:
                write_log("Try roll back", "OK")
                install_old_saved_version()
                write_log("Success roll back", "OK")
                system_action('restart')

        elif change_resource_or_actions == '':
            show_decryption_data(generic_key, 'resource')

        else:
            s = 0
            for resource_in_folder in os.listdir(FOLDER_WITH_RESOURCES):  # Вывод данных ресурса
                s += 1
                if s == int(change_resource_or_actions):
                    system_action('clear')
                    show_decryption_data(generic_key, 'resource')

                    path_to_resource = FOLDER_WITH_RESOURCES + resource_in_folder
                    resource_from_file = path_to_resource + '/' + FILE_RESOURCE
                    login_from_file = path_to_resource + '/' + FILE_LOGIN
                    password_from_file = path_to_resource + '/' + FILE_PASSWORD

                    def template_print_decryption_data(data_type, value):
                        print(BLUE, data_type, YELLOW, dec_aes(value, generic_key), DEFAULT_COLOR)

                    template_print_decryption_data(
                        'Resource --->', resource_from_file)
                    template_print_decryption_data(
                        'Login ------>', login_from_file)
                    template_print_decryption_data(
                        'Password --->', password_from_file)

    except ValueError as error:
        write_log(error, "pass")
        show_decryption_data(generic_key, 'resource')   # Показ ресурсов
    decryption_block(generic_key)  # Рекусрия под-главной функции
