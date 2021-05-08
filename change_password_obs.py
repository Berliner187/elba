from main import *

from csv import DictReader, DictWriter
from enc_obs import enc_aes, dec_aes

from werkzeug.security import generate_password_hash, check_password_hash
from stdiomask import getpass

from time import sleep
from shutil import copyfile
import os


__version__ = '2.0.0 ON DEVELOPMENT STAGE'


def change_master_password():
    system_action('clear')

    def user_input_password():
        print(BLUE + '\n Minimum password length 8 characters' + DEFAULT_COLOR)
        user_password = getpass('\n Password: ')
        user_confirm_password = getpass(' Confirm password: ')
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
        confirm_master_password = getpass(YELLOW + ' -- Enter your master-password: ' + DEFAULT_COLOR)
        open_file_with_hash = open(FILE_WITH_HASH).readline()
        check_master_password = check_password_hash(open_file_with_hash, confirm_master_password)

        if check_master_password == bool(False):
            print(RED + '\n --- Wrong password --- ' + DEFAULT_COLOR)
            sleep(1)
            system_action('restart')
        else:
            print(GREEN + ' -- Success confirm -- ' + DEFAULT_COLOR)
            sleep(.6)
            system_action('clear')
            print(BLUE + '\n   Pick a new master-password \n' + DEFAULT_COLOR)
            new_master_password = user_input_password()
            cnt = 0
            with open(FILE_FOR_RESOURCE, mode='r', encoding='utf-8') as saved_resource:  # Выгружается старый файл
                reader_resources = DictReader(saved_resource, delimiter=',')
                mas_res, mas_log, mas_pas = [], [], []
                new_file_data_base = 'main_data.dat'
                for item in reader_resources:
                    cnt += 1    # Счетчик для нового файла
                    # Дешифрование старым паролем
                    dec_res = dec_aes(item["resource"], confirm_master_password)
                    dec_log = dec_aes(item["login"], confirm_master_password)
                    dec_pas = dec_aes(item["password"], confirm_master_password)

                    # Шифрование новым паролем
                    enc_res = enc_aes(dec_res, new_master_password)
                    enc_log = enc_aes(dec_log, new_master_password)
                    enc_pas = enc_aes(dec_pas, new_master_password)

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
            copyfile(new_file_data_base, FILE_FOR_RESOURCE)    # Перезапись старого файла новым
            os.system('rm ' + new_file_data_base)   # Удаление нового файла

            new_hash = generate_password_hash(new_master_password)
            with open(FILE_WITH_HASH, 'w') as hash_pas:
                hash_pas.write(new_hash)
                hash_pas.close()

        system_action('restart')
    except TypeError:
        pass
