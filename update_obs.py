from main import *

import os
from time import sleep


__version__ = '1.2.0'   # Версия модуля


# Модули для работы программы
stock_modules = ['datetime_obs.py', 'enc_obs.py', 'logo_obs.py',
                 'del_resource_obs.py', 'notes_obs.py',
                 'change_password_obs.py', 'confirm_password_obs.py']


def update():   # Обновление программы
    main_file = 'main.py'  # Главный файл программы
    new_folder_el = 'elba/'  # Новая папка из репозитория проекта
    remove_main_folder = 'rm -r ' + new_folder_el + ' -f'  # Удаление новой папки
    download_from_repository()  # Загрузка проекта из репозитория

    cnt_modules = 0     # Счетчик отсутствующих модулей
    file_type = 'obs.py'    # Модули заканчиваются на *obs.py
    any_file = os.listdir('.')  # Поиск в текущей папке
    modules = []    # Массив для установленных модулей
    for file in any_file:   # Итерация модулей
        if file.endswith(file_type):
            modules.append(file)
    for j in range(len(stock_modules)):
        if stock_modules[j] not in modules:
            cnt_modules += 1

    def actions_for_install(program_file):  # Действия для установки
        os.system('cp ' + new_folder_el + program_file + ' . ; ')

    if cnt_modules != 0:
        system_action('clear')

        def text_about_missing(text):
            print(RED + '       ' + text + '\n' + DEFAULT_COLOR)
        if cnt_modules == 1:
            text_about_missing('Missing module')
        elif cnt_modules > 1:
            text_about_missing('Missing modules')
        for item in range(len(stock_modules)):
            def template_text_modules(color, message):
                print('[', color, message, DEFAULT_COLOR, ']', stock_modules[item])
            if stock_modules[item] not in modules:  # Вывод отсутствующего модуля
                template_text_modules(RED, 'Missing module')
                sleep(.8)
            else:   # Вывод состояния ОК
                template_text_modules(GREEN, 'OK')
                sleep(.5)

        for i in range(len(stock_modules)):
            actions_for_install(stock_modules[i])

        os.system(remove_main_folder)
        print(GREEN + '\n The missing module has been installed! \n\n' + DEFAULT_COLOR)
        sleep(1)
        system_action('restart')

    if os.path.exists(new_folder_el):
        # Обновление, если суммы файлов не совпадают
        if os.path.getsize(main_file) != os.path.getsize(new_folder_el + main_file):
            print(GREEN + '\n   A new version of the program is available ' + DEFAULT_COLOR)
            install_or_no = input(yellow + ' - Install new version program? (y/n): ' + DEFAULT_COLOR)
            if install_or_no == 'y':

                actions_for_install(main_file)
                actions_for_install('update_obs.py')
                for i in range(len(stock_modules)):
                    actions_for_install(stock_modules[i])
                system_action('restart')
            else:
                os.system(remove_main_folder)
        else:
            system_action('clear')
            print(yellow + ' -- You are using the latest version of the program -- ' + DEFAULT_COLOR)
            os.system(remove_main_folder)
            sleep(.7)
    else:
        print(yellow + ' - New folder not found... ' + DEFAULT_COLOR)
        download_from_repository()
