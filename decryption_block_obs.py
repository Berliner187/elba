# -*- coding: UTF-8 -*-

"""
    Модуль, отвечающий за управление функциями программы.
    В этом модуле пользователь выбирает дейсвия, необходимые для выполнения,
    а decryption_block передает управление другим модулям.
"""

from del_object_obs import delete_object
from notes_obs import notes
from change_password_obs import change_master_password
from actions_with_password_obs import choice_generation_or_save_self_password
from enc_obs import dec_aes, actions_with_encryption_files
from show_dec_data_obs import show_decryption_data
from update_obs import update, install_old_saved_version

from main import *


__version__ = '2.3.1'


def decryption_block(generic_key):
    """ Цикл с выводом сохраненных ресурсов и выбор действий """
    change_resource_or_actions = input('\n Change action: ')   # Выбор действия
    try:
        if change_resource_or_actions == '-a':  # Добавление нового ресурса
            system_action('clear')
            template_some_message(BLUE, '   --- Add new resource ---   ')
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
            template_some_message(BLUE, ' --- ELBA CLOSED ---')
            write_log("Exit", "OK")
            quit()

        elif change_resource_or_actions == '-r':  # Перезапуск
            system_action('clear')
            template_some_message(GREEN, ' --- Restart ---')
            sleep(.2)
            write_log("Restart", "OK")
            system_action('restart')

        elif change_resource_or_actions == '-c':    # Смена мастер-пароля
            change_master_password()
            write_log("Change password", "OK")

        elif change_resource_or_actions == '-d':    # Удаление ресурса
            delete_object('resource')
            show_decryption_data(generic_key, 'resource')
            write_log("Delete resource", "OK")

        elif change_resource_or_actions == '-n':    # Добавление заметок
            show_decryption_data(generic_key, 'note')
            notes(generic_key)
            write_log("Go to notes", "OK")

        elif change_resource_or_actions == '-f':    # Шифрование файлов
            # Переписать под show_dec_data_obs
            actions_with_encryption_files(generic_key)
            show_decryption_data(generic_key, 'resource')

        elif change_resource_or_actions == '-z':    # Удаление всех данных
            system_action('clear')
            template_some_message(RED, ' - Are you sure you want to delete all data? - ')
            change_yes_or_no = input(YELLOW + ' - Remove ALL data? (y/n): ' + DEFAULT_COLOR)
            if change_yes_or_no == 'y':
                template_remove_folder(FOLDER_WITH_DATA)
                system_action('clear')
                quit()

        elif change_resource_or_actions == '-i':
            from get_size_obs import size_all, get_versions
            get_versions()
            size_all()
            write_log("Get size and versions", "OK")
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
                write_log("Check logs", "OK")
            except KeyError as error:
                write_log(error, "FAILED")
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

        elif change_resource_or_actions == '-s':
            system_action('clear')
            template_some_message(GREEN, ' --- Settings ---')
            lines_set = [
                f'{BLUE}1. {YELLOW}Customize colors accent'
            ]
            for line in lines_set:
                print(line)
            change_in_settings = input(' - Change setting by number: ')
            if change_in_settings == '1':
                system_action('clear')

                dic_colors = ''
                with open(FILE_SETTINGS_COLOR, 'r') as f:
                    for i in f.readlines():
                        dic_colors = i
                dic_colors = eval(dic_colors)

                cnt = 0
                for item in dic_colors:
                    cnt += 1
                    print(f"{YELLOW}{cnt}. "
                          f"{DEFAULT_COLOR}{item} = {format_hex_color(dic_colors[item])}{dic_colors[item]}")

                template_some_message(BLUE, ' -- Color emphasis will change after restarting the program --')
                setting_colors = int(input(YELLOW + ' - Choose a color to change the accent: '))
                cnt = 0
                for select in dic_colors:
                    cnt += 1
                    if setting_colors == cnt:
                        while True:
                            new_color = input(f'{GREEN} - Input new color in HEX: {DEFAULT_COLOR}#')
                            if len(new_color) == 6:
                                break
                            else:
                                template_some_message(RED, ' - HEX format should consist of 6 characters -')
                        dic_colors[select] = f'#{new_color}'.upper()
                        with open(FILE_SETTINGS_COLOR, 'w+') as f:
                            f.write(str(dic_colors))
                            f.close()
                        system_action('clear')
                        template_some_message(GREEN, ' - Successfully changed color accent -')
                        sleep(1)
            show_decryption_data(generic_key, 'resource')

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

    except ValueError:
        show_decryption_data(generic_key, 'resource')   # Показ ресурсов
    decryption_block(generic_key)  # Рекусрия под-главной функции
