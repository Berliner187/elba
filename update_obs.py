from main import system_action, show_decryption_data, decryption_block
from enc_obs import dec_data
import os


yellow, mc = "\033[33m", "\033[0m"

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
            actions_for_install('stars_obs.py')
            actions_for_install('enc_obs.py')
            actions_for_install('datetime.py')
            actions_for_install('logo_obs.py')
            actions_for_install('update_obs.py')

            system_action('either')
        else:
            os.system(remove_main_folder)
    else:
        system_action('clear')
        print(yellow + ' -- Nothing to upgrade, you have latest update -- ' + mc)
        os.system(remove_main_folder)
        sleep(.7)