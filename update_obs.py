import os
from time import sleep
from enc_obs import dec_data
from main import system_action, show_decryption_data, decryption_block


yellow, mc = "\033[33m", "\033[0m"
used_modules = ['stars_obs.py', 'datetime_obs.py', 'enc_obs.py', 'logo_obs.py', 'update_obs.py']


def update(master_password, status):
    main_file = 'main.py'  # Главный файл программы
    remove_main_folder = 'rm -r elba/ -f'
    os.system('git clone https://github.com/Berliner187/elba')
    system_action('clear')

    if os.path.getsize(main_file) != os.path.getsize('elba/' + main_file):
        install_or_no = input(yellow + ' - Install? (y/n): ' + mc)
        new_folder_pm = 'elba/'    # Новая папка из репозитория проекта
        if install_or_no == 'y':

            def actions_for_install(file):  # Действия для установки
                os.system('cp ' + new_folder_pm + file + ' . ; ')

            actions_for_install(main_file)
            actions_for_install(used_modules[0])
            actions_for_install(used_modules[1])
            actions_for_install(used_modules[2])
            actions_for_install(used_modules[3])
            actions_for_install(used_modules[4])

            system_action('either')
        else:
            os.system(remove_main_folder)
    else:
        system_action('clear')
        print(yellow + ' -- Nothing to upgrade, you have latest update -- ' + mc)
        os.system(remove_main_folder)
        sleep(.7)
