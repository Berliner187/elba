from main import *

import os
from time import sleep


__version__ = '1.2.4'   # Версия модуля


# Модули для работы программы
stock_modules = ['datetime_obs.py', 'enc_obs.py', 'logo_obs.py',
                 'del_resource_obs.py', 'notes_obs.py', 'get_size_obs.py',
                 'change_password_obs.py', 'confirm_password_obs.py']


def update():   # Обновление программы
    main_file = 'main.py'
    new_folder_el = 'elba/'
    remove_main_folder = 'rm -r ' + new_folder_el + ' -f'  # Удаление новой папки
    download_from_repository()  # Загрузка проекта из репозитория

    # Проверка отсутствующих модулей
    cnt_modules = 0
    file_type = 'obs.py'
    any_file = os.listdir('.')
    installed_modules = []
    for file in any_file:
        if file.endswith(file_type):
            installed_modules.append(file)
    for j in range(len(stock_modules)):
        if stock_modules[j] not in installed_modules:
            cnt_modules += 1    # Счет отсутствующих модулей

    def actions_for_install(program_file):  # Действия для установки
        os.system('cp ' + new_folder_el + program_file + ' . ; ')

    if cnt_modules != 0:
        system_action('clear')

        if cnt_modules == 1:
            print(RED + '  Missing module \n' + DEFAULT_COLOR)
        elif cnt_modules > 1:
            print(RED + '  Missing modules \n' + DEFAULT_COLOR)
        for item in range(len(stock_modules)):
            def template_text_modules(color, message):
                print('[', color, message, DEFAULT_COLOR, ']', stock_modules[item])
            if stock_modules[item] not in installed_modules:  # Вывод отсутствующего модуля
                template_text_modules(RED, 'FAILED')
                sleep(.5)
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
            install_or_no = input(YELLOW + ' - Install new version program? (y/n): ' + DEFAULT_COLOR)
            if install_or_no == 'y':

                actions_for_install(main_file)
                actions_for_install('update_obs.py')
                for i in range(len(stock_modules)):
                    actions_for_install(stock_modules[i])
                print(GREEN + "  - Successfully installed! - ")
                system_action('restart')
                os.system(remove_main_folder)
            else:
                os.system(remove_main_folder)
        else:
            system_action('clear')
            print(YELLOW + ' -- You are using the latest version of the program -- ' + DEFAULT_COLOR)
            os.system(remove_main_folder)
            sleep(.7)
    else:
        print(YELLOW + ' - New folder not found... ' + DEFAULT_COLOR)
        download_from_repository()
