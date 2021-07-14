from main import *
from main import __version__ as elba_version

import os
from time import sleep

__version__ = '1.5.4'  # Версия модуля


main_file = 'main.py'
new_folder_el = 'elba/'


def update():  # Обновление программы
    download_from_repository()  # Загрузка проекта из репозитория

    status_modules = check_modules()

    def template_for_install(program_file):  # Действия для установки
        os.system('mv ' + new_folder_el + program_file + ' . ')

    def template_question(text):
        question = input(YELLOW + ' - ' + text + ' (y/n): ' + DEFAULT_COLOR)
        return question

    def message_about_status_modules():
        template_some_message(YELLOW, " - Check Modules - ")
        system_action('clear')
        installed_modules = []
        for file in os.listdir('.'):
            if file.endswith('obs.py'):
                installed_modules.append(file)
        for item_mod in range(len(stock_modules)):
            def template_text_modules(color, message):
                print('[', color, message, DEFAULT_COLOR, ']', stock_modules[item_mod])
            if stock_modules[item_mod] not in installed_modules:
                template_text_modules(RED, 'FAILED')
                write_log(stock_modules[item_mod], 'FAILED')
                sleep(.2)
            else:
                template_text_modules(GREEN, 'OK')
                sleep(.2)

    if status_modules != 0:
        system_action('clear')
        message_about_status_modules()

        for i in range(len(stock_modules)):
            template_for_install(stock_modules[i])

        system_action('clear')
        template_remove_folder(new_folder_el)
        message_about_status_modules()
        print(GREEN + '\n The missing module has been installed! \n\n' + DEFAULT_COLOR)
        sleep(1)
        system_action('restart')
    else:
        if os.path.exists(new_folder_el):

            def template_for_copy(item_program):
                os.system('cp ' + item_program + ' ' + OLD_ELBA + elba_version)

            # Создание резервной копии
            if os.path.exists(OLD_ELBA) is False:
                os.mkdir(OLD_ELBA)
            if os.path.exists(OLD_ELBA + elba_version) is False:
                os.mkdir(OLD_ELBA + elba_version)
                # Копирование файлов программы
                for item in os.listdir('.'):
                    if item.endswith('.py'):
                        template_for_copy(item)
                # Копирование данных юзера
                os.system("cp -a " + FOLDER_WITH_DATA + ' ' + OLD_ELBA + elba_version + '/')

            if os.path.getsize(main_file) != os.path.getsize(new_folder_el + main_file):
                print(GREEN + '\n   A new version of the program is available ' + DEFAULT_COLOR)
                install_or_no = template_question(' - Install new version program?')

                if install_or_no == 'y':
                    template_for_install(main_file)
                    template_for_install('update_obs.py')
                    for i in range(len(stock_modules)):
                        template_for_install(stock_modules[i])
                    system_action('clear')
                    print(GREEN + "\n\n    - Successfully installed! - ")
                    sleep(.7)
                    write_log('Upgrade', 'OK')

                template_remove_folder(new_folder_el)
                system_action('restart')
            else:
                system_action('clear')
                template_some_message(YELLOW, ' -- You are using the latest version of the program -- ')

                template_for_install('update_obs.py')
                for module in stock_modules:
                    if os.path.getsize(new_folder_el + module) != os.path.getsize(module):
                        template_for_install(module)
                        write_log('Upgrade ' + module, 'OK')

                template_remove_folder(new_folder_el)
                sleep(.7)
        else:
            print(YELLOW + ' - New folder not found... ' + DEFAULT_COLOR)
            write_log('New folder not exist', 'ERROR: Not Found Folder')
            sleep(1)
            download_from_repository()


def install_old_saved_version():
    s = 0
    system_action('clear')
    for version in os.listdir(OLD_ELBA):
        s += 1
        print(str(s), '-', YELLOW + version + DEFAULT_COLOR)

    print(BLUE + "\n\n  - Change version by number - " + DEFAULT_COLOR)
    change = int(input(YELLOW + "(1-" + str(s) + "): " + DEFAULT_COLOR))
    if change == '-z':
        template_remove_folder(OLD_ELBA)
    cnt = 0
    for need_version_folder in os.listdir(OLD_ELBA):
        cnt += 1
        if cnt == change:
            for item in os.listdir(OLD_ELBA + need_version_folder):
                os.system('cp ' + OLD_ELBA + need_version_folder + '/' + item + ' ' + '.')
            template_remove_folder(FOLDER_WITH_DATA)
            os.system("cp -a " + OLD_ELBA + need_version_folder + '/' + FOLDER_WITH_DATA + '/' + ' ' + '.')

    print(GREEN + ' - Success roll back! - ' + DEFAULT_COLOR)
    sleep(1)
