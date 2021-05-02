# Локальные модули
from main import system_action, fields_for_main_data
from main import main_folder, file_date_base, file_hash_password
from main import YELLOW, BLUE, PURPLE, GREEN, RED, DEFAULT_COLOR
from csv import DictReader, DictWriter
from enc_obs import enc_data, dec_data
# Сторонние модули
from werkzeug.security import generate_password_hash, check_password_hash
from stdiomask import getpass
# Встроенные модули
from time import sleep
from shutil import copyfile
import os


__version__ = '1.1.0'


def change_master_password():
    system_action('clear')

    def user_input_password():
        print(BLUE + '\n Minimum password length 8 characters' + DEFAULT_COLOR)
        user_password = getpass('\n Password: ')
        user_confirm_password = getpass(' Confirm password: ')  # hide_password(' Confirm password: ')
        cnt_trying = 0
        if (user_password != user_confirm_password) or (len(user_password) or len(user_confirm_password)) < 8:
            print(red + '\n Error of confirm. Try again \n' + DEFAULT_COLOR)
            cnt_trying += 1
            if cnt_trying == 1:
                quit()
        elif (user_password == user_confirm_password) and (len(user_password) and len(user_confirm_password)) >= 8:
            return user_confirm_password
    # Сверяются хеши паролей
    try:
        confirm_master_password = getpass(yellow + ' -- Enter your master-password: ' + DEFAULT_COLOR)
        open_file_with_hash = open(file_hash_password).readline()
        check_master_password = check_password_hash(open_file_with_hash, confirm_master_password)

        if check_master_password == bool(False):
            print(red + '\n --- Wrong password --- ' + DEFAULT_COLOR)
            sleep(1)
            system_action('restart')
        else:
            print('       [' + green + ' OK ' + DEFAULT_COLOR + ']')
            sleep(.6)
            system_action('clear')
            print(BLUE + '\n   Pick a new master-password \n' + DEFAULT_COLOR)
            new_master_password = user_input_password()
            cnt = 0
            with open(file_date_base, mode='r', encoding='utf-8') as saved_resource:  # Выгружается старый файл
                reader_resources = DictReader(saved_resource, delimiter=',')
                mas_res, mas_log, mas_pas = [], [], []
                new_file_data_base = 'main_data.dat'
                for item in reader_resources:
                    cnt += 1    # Счетчик для нового файла
                    # Дешифрование старым паролем
                    dec_res = dec_data(item["resource"], confirm_master_password)
                    dec_log = dec_data(item["login"], confirm_master_password)
                    dec_pas = dec_data(item["password"], confirm_master_password)

                    # Шифрование новым паролем
                    enc_res = enc_data(dec_res, new_master_password)
                    enc_log = enc_data(dec_log, new_master_password)
                    enc_pas = enc_data(dec_pas, new_master_password)

                    # Добавление зашифрованных данных в массивы
                    mas_res.append(enc_res)
                    mas_log.append(enc_log)
                    mas_pas.append(enc_pas)

            with open(new_file_data_base, mode="a", encoding='utf-8') as data:  # Запись в новый файл
                new_writer = DictWriter(data, fieldnames=fields_for_main_data)
                new_writer.writeheader()
                for i in range(cnt):
                    new_writer.writerow({
                        fields_for_main_data[0]: mas_res[i],
                        fields_for_main_data[1]: mas_log[i],
                        fields_for_main_data[2]: mas_pas[i]
                    })
            copyfile(new_file_data_base, file_date_base)    # Перезапись старого файла новым
            os.system('rm ' + new_file_data_base)   # Удаление нового файла

            new_hash = generate_password_hash(new_master_password)
            with open(file_hash_password, 'w') as hash_pas:
                hash_pas.write(new_hash)
                hash_pas.close()

        system_action('restart')
    except TypeError:
        pass
