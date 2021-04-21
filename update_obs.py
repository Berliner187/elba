import os
from time import sleep
from main import system_action, show_decryption_data, decryption_block


__version__ = '1.1.1'   # Версия модуля

# Цвета
yellow, blue, purple = "\033[33m", "\033[36m", "\033[35m"
green, mc, red = "\033[32m", "\033[0m", "\033[31m"
# Модули для работы программы
stock_modules = ['datetime_obs.py', 'enc_obs.py', 'logo_obs.py',
                 'stars_obs.py', 'del_resource_obs.py', 'notes_obs.py',
                 'change_password_obs.py', 'confirm_password_obs.py']


def update():   # Обновление программы
    main_file = 'main.py'  # Главный файл программы
    new_folder_el = 'elba/'    # Новая папка из репозитория проекта
    remove_main_folder = 'rm -r elba/ -f'   # Удаление новой папки
    os.system('git clone https://github.com/Berliner187/elba')  # Репозиторий
    system_action('clear')

    def actions_for_install(program_file):  # Действия для установки
        os.system('cp ' + new_folder_el + program_file + ' . ; ')

    system_action('clear')

    cnt_modules = 0
    file_type = 'obs.py'
    any_file = os.listdir('.')
    modules = []
    for file in any_file:
        if file.endswith(file_type):
            modules.append(file)
    for j in range(len(stock_modules)):
        if stock_modules[j] not in modules:
            cnt_modules += 1

    if cnt_modules != 0:
        system_action('clear')
        def text_about_missing(text):
            print(red + '       ' + text + '\n' + mc)
        if cnt_modules == 1:
            text_about_missing('Missing module')
        elif cnt_modules > 1:
            text_about_missing('Missing modules')
        for item in range(len(stock_modules)):
            if stock_modules[item] not in modules:
                print('[', red, 'Missing module', mc, ']', stock_modules[item])
                sleep(.8)
            else:
                print('[', green, 'OK', mc, ']', stock_modules[item])
                sleep(.5)
        for i in range(len(stock_modules)):
            actions_for_install(stock_modules[i])
        print(green + '\n The missing module has been installed! \n\n' + mc)
        sleep(1)
        os.system(remove_main_folder)
        system_action('restart')
    else:
        quit()

    if os.path.getsize(main_file) != os.path.getsize(new_folder_el + main_file):

        print(green + '\n   A new version of the program is available ' + mc)
        install_or_no = input(yellow + ' - Install new version program? (y/n): ' + mc)
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
        print(yellow + ' -- You are using the latest version of the program -- ' + mc)
        os.system(remove_main_folder)
        sleep(.7)
