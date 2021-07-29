from main import *
from main import __version__ as elba_version

import os
from time import sleep


__version__ = '1.6.2'


def get_peculiarities_copy(type_copy):
    """ Поддержка синтаксиса командных оболочек Linux, MacOS X и Windows """
    if type_copy == 'dir':
        if os.name == 'nt':
            peculiarities_copy = 'xcopy /y /o /e '
        else:
            peculiarities_copy = 'cp -r '
        return peculiarities_copy
    elif type_copy == 'file':
        if os.name == 'nt':
            peculiarities_copy = 'copy '
        else:
            peculiarities_copy = 'cp '
        return peculiarities_copy
    elif type_copy == 'move':
        if os.name == 'nt':
            peculiarities_move = 'move '
        else:
            peculiarities_move = 'mv '
        return peculiarities_move


def template_for_install(program_file):
    """ Шаблон установки файлов программы """
    os.system(get_peculiarities_copy('move') + FOLDER_ELBA + program_file + ' . ')


def template_question(text):
    """ Шаблон вопросов от программы """
    question = input(YELLOW + ' - ' + text + ' (y/n): ' + DEFAULT_COLOR)
    return question


def update():
    """ Обновление программы и модулей """
    download_from_repository()  # Загрузка Эльбы из репозитория

    status_modules = check_modules()
    main_file = 'main.py'

    def get_installed_modules():
        installed_modules = []
        for file in os.listdir('.'):
            if file.endswith('obs.py'):
                installed_modules.append(file)
        return installed_modules

    def message_about_status_modules():
        """ Вывод показателей о состоянии модулей """
        template_some_message(YELLOW, " - Check Modules -")
        system_action('clear')
        installed_modules = get_installed_modules()
        cnt_missing_mod = 0
        for item_mod in range(len(stock_modules)):
            def template_text_modules(color, message):
                print('[', color, message, DEFAULT_COLOR, ']', stock_modules[item_mod])
            if stock_modules[item_mod] not in installed_modules:
                template_text_modules(RED, 'FAILED')
                write_log(stock_modules[item_mod], 'FAILED')
                sleep(.2)
                cnt_missing_mod += 1
            else:
                template_text_modules(GREEN, 'OK')
                sleep(.2)
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
        if os.path.exists(FOLDER_ELBA):

            def template_for_copy(item_program):
                os.system(get_peculiarities_copy('file') + item_program + ' ' + OLD_ELBA + elba_version)

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
                os.system(get_peculiarities_copy('dir') + FOLDER_WITH_DATA + ' ' + OLD_ELBA + elba_version + '/')
            # Условие установки новой версии программы
            if os.path.getsize(main_file) != os.path.getsize(FOLDER_ELBA + main_file):
                template_some_message(GREEN, ' A new version of the program is available ')
                install_or_no = template_question(' - Install new version program?')

                if install_or_no == 'y':
                    template_for_install(main_file)
                    template_for_install('update_obs.py')
                    for i in range(len(stock_modules)):
                        template_for_install(stock_modules[i])
                    system_action('clear')
                    template_some_message(GREEN, "  - Successfully installed! -")
                    sleep(.7)
                    write_log('Upgrade', 'OK')

                template_remove_folder(FOLDER_ELBA)
                system_action('restart')
            else:
                system_action('clear')
                template_some_message(YELLOW, ' -- You are using the latest version of the program -- ')

                # Установка обновленных модулей
                template_for_install('update_obs.py')
                for module in stock_modules:
                    if os.path.getsize(FOLDER_ELBA + module) != os.path.getsize(module):
                        template_for_install(module)
                        write_log('Upgrade: ' + module, 'OK')

                template_remove_folder(FOLDER_ELBA)
                sleep(.7)
        else:
            template_some_message(YELLOW, ' - New folder not found... -')
            write_log('New folder not exist', 'PASS')
            sleep(1)
            change_download_or_no = template_question('Try download from repository?')
            if change_download_or_no == 'y':
                download_from_repository()
            else:
                quit()


def install_old_saved_version():
    """ Откат к сохраненым версиям """
    s = 0
    system_action('clear')
    for version in os.listdir(OLD_ELBA):
        s += 1
        print(str(s), '-', YELLOW + version + DEFAULT_COLOR)

    template_some_message(BLUE, "  - Change version by number - ")
    change = int(input(YELLOW + "(1-" + str(s) + "): " + DEFAULT_COLOR))
    if change == '-z':
        template_remove_folder(OLD_ELBA)
    cnt = 0
    for need_version_folder in os.listdir(OLD_ELBA):
        cnt += 1
        if cnt == change:
            for item in os.listdir(OLD_ELBA + need_version_folder):
                if item.endswith('.py'):
                    os.system(get_peculiarities_copy('file') + OLD_ELBA + need_version_folder + '/' + item + ' .')
            template_remove_folder(FOLDER_WITH_DATA)
            os.system(
                get_peculiarities_copy('dir') + OLD_ELBA + need_version_folder + '/' + FOLDER_WITH_DATA + '/' + ' .'
            )
    system_action('clear')
    template_some_message(GREEN, '  --- Success roll back! --- ')
    write_log('Roll back', 'Done')
    sleep(1)
