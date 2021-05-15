from main import *
from main import __version__ as elba_version

import os
from time import sleep

__version__ = '1.4.2'  # Версия модуля


main_file = 'main.py'
new_folder_el = 'elba/'


def update():  # Обновление программы
    download_from_repository()  # Загрузка проекта из репозитория

    # Проверка отсутствующих модулей
    cnt_modules = 0
    file_type = 'obs.py'
    any_file = os.listdir('.')
    installed_modules = []
    for file in any_file:
        if file.endswith(file_type):
            installed_modules.append(file)

    for j in range(len(stock_modules)):  # Счет отсутствующих модулей
        if stock_modules[j] not in installed_modules:
            cnt_modules += 1

    def template_for_install(program_file):  # Действия для установки
        os.system('mv ' + new_folder_el + program_file + ' . ')

    def template_question(text):
        question = input(YELLOW + ' - ' + text + ' (y/n): ' + DEFAULT_COLOR)
        return question

    def template_red_text(text):
        print(RED, text, ' \n', DEFAULT_COLOR)

    if cnt_modules != 0:
        system_action('clear')

        if cnt_modules == 1:
            template_red_text('Missing module')
            write_log('MissingModule', 'ERROR')
        elif cnt_modules > 1:
            template_red_text('Missing modules')
            write_log('MissingModules', 'ERROR')

        for item in range(len(stock_modules)):
            def template_text_modules(color, message):
                print('[', color, message, DEFAULT_COLOR, ']', stock_modules[item])

            if stock_modules[item] not in installed_modules:
                template_text_modules(RED, 'FAILED')
                write_log(stock_modules[item], 'FAILED')
                sleep(.5)
            else:
                template_text_modules(GREEN, 'OK')
                sleep(.5)

        for i in range(len(stock_modules)):
            template_for_install(stock_modules[i])

        template_remove_folder(new_folder_el)
        print(GREEN + '\n The missing module has been installed! \n\n' + DEFAULT_COLOR)
        sleep(1)
        system_action('restart')

    if os.path.exists(new_folder_el):

        def template_for_copy(item_program):
            os.system('cp ' + item_program + ' ' + old_elba + elba_version)

        # Создание резервной копии
        if os.path.exists(old_elba) is False:
            os.mkdir(old_elba)
        if os.path.exists(old_elba + elba_version) is False:
            os.mkdir(old_elba + elba_version)
            for item in os.listdir('.'):
                if item.endswith('.py'):
                    template_for_copy(item)

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
    def template_install_old(version_old_folder):
        for item in os.listdir(old_elba + version_old_folder):
            os.system('cp ' + old_elba + version_old_folder + '/' + item + ' ' + '.')
    s = 0
    system_action('clear')
    for version in os.listdir(old_elba):
        s += 1
        print(str(s), '-', YELLOW + version + DEFAULT_COLOR)
    print(BLUE + "\n\n  - Change version by number - " + DEFAULT_COLOR)
    change = int(input(YELLOW + "(1-" + str(s) + "): " + DEFAULT_COLOR))
    cnt = 0
    for need_version_folder in os.listdir(old_elba):
        cnt += 1
        if cnt == change:
            template_install_old(need_version_folder)
    print(GREEN + ' - Success roll back! - ' + DEFAULT_COLOR)
    sleep(1)
