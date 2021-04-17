import os
from time import sleep
from main import system_action, show_decryption_data, decryption_block


__version__ = '1.0.5'   # Версия модуля


yellow, blue, purple, green, mc, red = "\033[33m", "\033[36m", "\033[35m", "\033[32m", "\033[0m", "\033[31m"
stock_modules = ['datetime_obs.py', 'enc_obs.py', 'logo_obs.py',
                 'update_obs.py', 'stars_obs.py', 'del_resource_obs.py']


def update():
    main_file = 'main.py'  # Главный файл программы
    new_folder_el = 'elba/'    # Новая папка из репозитория проекта
    remove_main_folder = 'rm -r elba/ -f'
    os.system('git clone https://github.com/Berliner187/elba')
    system_action('clear')

    print(blue + '\n        Check modules \n\n' + mc)
    file_type = 'obs.py'
    any_file = os.listdir('.')
    modules = []
    cnt_mod = 0
    for file in any_file:
        if file.endswith(file_type):
            modules.append(file)
    for i in range(len(stock_modules)):
        if stock_modules[i] not in modules:
            print('[', red, 'Missing module', mc, ']', stock_modules[i])
            cnt_mod += 1
            sleep(.8)
        else:
            print('[', green, 'OK', mc, ']', stock_modules[i])
            sleep(.5)

    system_action('clear')

    if os.path.getsize(main_file) != os.path.getsize(new_folder_el + main_file) or cnt_mod != 0:
        install_or_no = input(yellow + ' - Install? (y/n): ' + mc)
        if install_or_no == 'y':

            def actions_for_install(program_file):  # Действия для установки
                os.system('cp ' + new_folder_el + program_file + ' . ; ')

            actions_for_install(main_file)
            for i in range(len(stock_modules)):
                actions_for_install(stock_modules[i])

            system_action('either')
        else:
            os.system(remove_main_folder)
    else:
        system_action('clear')
        print(yellow + ' -- Nothing to upgrade, you have latest update -- ' + mc)
        os.system(remove_main_folder)
        sleep(.7)
