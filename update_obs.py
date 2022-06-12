from main import *
from main import __version__ as elba_version

import os
from time import sleep


__version__ = '0.10-05'

MAIN_FILE = 'main.py'


def update():
    """ Обновление программы и модулей """
    download_from_repository()  # Загрузка Эльбы из репозитория

    status_modules = check_modules()

    def get_info_about_modules(color, message, mod):
        """ Отображение актуальности модулей """
        print("[ {:s}{:^4s}{:s} ] - {:s}".format(color, message, ACCENT_4, mod))

    def get_installed_modules():
        installed_modules = []
        for file in os.listdir('.'):
            if file.endswith('obs.py'):
                installed_modules.append(file)
        return installed_modules

    def message_about_status_modules():
        """ Отображение текущего состояния модулей """
        system_action('clear')
        template_warning_message(ACCENT_1, "-- Check Modules --".upper())
        installed_modules = get_installed_modules()
        cnt_missing_mod = 0
        for item_mod in range(len(stock_modules)):
            if stock_modules[item_mod] not in installed_modules:
                get_info_about_modules(RED, 'FAIL', stock_modules[item_mod])
                write_log(stock_modules[item_mod], 'MISSING')
                cnt_missing_mod += 1
            else:
                get_info_about_modules(GREEN, 'OK', stock_modules[item_mod])
            sleep(.3)
        return cnt_missing_mod

    if status_modules != 0:
        system_action('clear')
        message_about_status_modules()

        for i in range(len(stock_modules)):
            template_for_install(stock_modules[i])

        system_action('clear')
        template_remove_folder(FOLDER_ELBA)
        cnt_missing_modules = message_about_status_modules()
        if cnt_missing_modules == 0:
            template_some_message(GREEN, 'The missing module has been installed!')
        else:
            template_some_message(RED, 'Not all modules were installed')
        sleep(1)
        system_action('restart')
    else:
        def template_for_copy(item_program):
            os.system(get_peculiarities_system('copy_file') + item_program + ' ' + OLD_ELBA + elba_version)

        if os.path.exists(FOLDER_ELBA):
            # Создание резервной копии
            if os.path.exists(OLD_ELBA) is False:
                os.mkdir(OLD_ELBA)
            if os.path.exists(OLD_ELBA + elba_version) is False:
                template_some_message(GREEN, "- Creating a backup -")
                os.mkdir(OLD_ELBA + elba_version)
                # Копирование файлов программы
                template_for_copy(FILE_WITH_SHA256)
                for item in os.listdir('.'):
                    if item.endswith('.py'):
                        template_for_copy(item)
                # Копирование данных юзера
                os.system(f"{get_peculiarities_system('copy_dir')}{FOLDER_WITH_DATA} {OLD_ELBA}{elba_version}/")
            else:
                template_some_message(ACCENT_1, "- Backup already exists -")
            sleep(1)

            # Условие установки новой версии программы
            if os.path.getsize(MAIN_FILE) != os.path.getsize(FOLDER_ELBA + MAIN_FILE):
                template_some_message(GREEN, 'A new version of the program is available')
                install_or_no = template_question('Install new version program?')

                if install_or_no == 'y':
                    template_for_install(MAIN_FILE)

                    for module in stock_modules:
                        if os.path.getsize(FOLDER_ELBA + module) != os.path.getsize(module):
                            get_info_about_modules(GREEN, 'UPDATE ', module)
                        else:
                            get_info_about_modules(ACCENT_1, 'REMAINS', module)
                        sleep(.2)

                    template_for_install('update_obs.py')
                    for i in range(len(stock_modules)):
                        template_for_install(stock_modules[i])
                    system_action('clear')
                    template_some_message(GREEN, "- Successfully installed! -")
                    sleep(.7)
                    authentication_check(False, True)
                    write_log('Upgrade', 'OK')
                else:
                    for module in stock_modules:
                        if os.path.getsize(FOLDER_ELBA + module) != os.path.getsize(module):
                            get_info_about_modules(GREEN, 'UPDATE ', module)
                            template_for_install(module)
                        else:
                            get_info_about_modules(ACCENT_1, 'REMAINS', module)
                        template_for_install('update_obs.py')
                        sleep(.2)

                template_remove_folder(FOLDER_ELBA)
                system_action('restart')
            else:
                system_action('clear')
                template_some_message(ACCENT_1, ' -- You are using the latest version of the program -- ')

                for module in stock_modules:
                    if os.path.getsize(FOLDER_ELBA + module) != os.path.getsize(module):
                        template_for_install(module)
                        write_log(f'Upgrade: {module}', 'OK')
                        get_info_about_modules(GREEN, 'UPDATE', module)
                    else:
                        get_info_about_modules(ACCENT_1, 'REMAINS', module)
                    sleep(.2)
                authentication_check(False, True)

                template_remove_folder(FOLDER_ELBA)
                sleep(.7)
        else:
            template_some_message(ACCENT_1, ' - New folder not found... -')
            write_log('New folder not exist', 'PASS')
            sleep(1)
            change_download_or_no = template_question('Try download from repository?')
            if change_download_or_no == 'y':
                download_from_repository()
            else:
                quit()


def trying_to_correct_an_error_in_execution(random_error):
    write_log(random_error, 'FAIL')
    template_warning_message(RED, '--- ERROR ---')
    print(random_error)
    sleep(1)
    system_action('clear')
    print(f"{ACCENT_3}"
          f'\n - Enter 1 to rollback'
          f'\n - Enter 2 to update')
    rollback_or_update = template_input('Select by number: ')
    if rollback_or_update == '1':  # Попытка откатиться
        template_some_message(RED, '-- You can try roll back --')
        rollback_obs.rollback()
    elif rollback_or_update == '2':  # Попытка обновиться
        write_log('Try update', 'RUN')
        update()
    else:
        system_action('clear')
        template_warning_message(RED, '--- ERROR IN CHANGE ---')
        sleep(1)
    system_action('restart')
