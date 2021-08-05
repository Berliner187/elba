# -*- coding: UTF-8 -*-

"""
    Модуль шифрования.
    Обеспечивает безопасность и сохранность всех данных пользователя.
    Доступные методы: AES и Base64
"""

from base64 import urlsafe_b64encode, urlsafe_b64decode
from base64 import b64encode, b64decode
import base64
import hashlib
import random
import os
from time import sleep
import datetime

from main import *

from stdiomask import getpass
from werkzeug.security import check_password_hash, generate_password_hash
from Crypto.Cipher import AES
import Crypto.Random


__version__ = '6.4.2'


class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Crypto.Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        code = cipher.encrypt((raw.encode()))
        return base64.b64encode(iv + code)

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


def enc_only_base64(message, key):
    """ Base64-based encryption """
    key, message = str(key), str(message)
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
    encryption = urlsafe_b64encode("".join(enc).encode()).decode()
    return encryption


def dec_only_base64(encryption, key):
    """ Base64-based decryption """
    key = str(key)
    dec = []
    message = urlsafe_b64decode(encryption).decode()
    for i in range(len(message)):
        key_c = key[i % len(key)]
        dec.append(chr((256 + ord(message[i]) - ord(key_c)) % 256))
    return "".join(dec)


def enc_aes(__file__, encryption, __key__):
    """ Шифрование и сохранение в файл """
    with open(__file__, 'wb') as enc_data:
        aes = AESCipher(__key__)
        payload = aes.encrypt(encryption)
        enc_data.write(payload)
        enc_data.close()

    with open(__file__, 'a') as write_space:
        write_space.write('\n')
        write_space.close()


def dec_aes(__file__, __key__):
    """ Дешифрование и сохранение в файл """
    with open(__file__, 'rb') as read_file:
        payload = read_file.readlines()
        for item in payload:
            aes = AESCipher(__key__)
            return aes.decrypt(item)


def enc_keyiv(keyiv, xzibit):
    keyiv = b64encode(keyiv)
    keyiv = str(keyiv)
    keyiv = keyiv[2:-1]
    aes = AESCipher(xzibit)
    return aes.encrypt(keyiv)


def dec_keyiv(enc_keyiv, xzibit):
    aes = AESCipher(xzibit)
    dec_key = aes.decrypt(enc_keyiv)
    keyiv = str.encode(dec_key)
    keyiv = b64decode(keyiv)
    return keyiv


def save_data_to_file(data_1, data_2, data_3, xzibit, type_data):

    def path_to_data_to_save_resource(enc_name_type_folder):
        return FOLDER_WITH_RESOURCES + enc_name_type_folder

    def path_to_data_to_save_note(enc_name_type_folder):
        return FOLDER_WITH_NOTES + enc_name_type_folder

    if type_data == 'resource':
        enc_name_resource_folder = enc_only_base64(data_1, xzibit) + '/'
        if os.path.exists(path_to_data_to_save_resource(enc_name_resource_folder)) is False:
            os.mkdir(path_to_data_to_save_resource(enc_name_resource_folder))

        resource_folder = path_to_data_to_save_resource(enc_name_resource_folder)
        login_folder = path_to_data_to_save_resource(enc_name_resource_folder)
        password_folder = path_to_data_to_save_resource(enc_name_resource_folder)

        resource_file = resource_folder + FILE_RESOURCE
        login_file = login_folder + FILE_LOGIN
        password_file = password_folder + FILE_PASSWORD

        enc_aes(resource_file, data_1, xzibit)
        enc_aes(login_file, data_2, xzibit)
        enc_aes(password_file, data_3, xzibit)

    if type_data == 'note':
        enc_name_note_folder = enc_only_base64(data_1, xzibit) + '/'
        if os.path.exists(path_to_data_to_save_note(enc_name_note_folder)) is False:
            os.mkdir(path_to_data_to_save_note(enc_name_note_folder))

        name_note = path_to_data_to_save_note(enc_name_note_folder)
        self_note = path_to_data_to_save_note(enc_name_note_folder)

        name_note_file = name_note + FILE_NOTE_NAME
        note_file = self_note + FILE_NOTE_ITSELF

        enc_aes(name_note_file, data_1, xzibit)
        enc_aes(note_file, data_2, xzibit)


class WorkWithUserFiles:

    def __init__(self, xzibit, type_work):
        self.xzibit = xzibit
        self.type_work = type_work

    def file_encryption_control(self):
        """ Управление шифрованием """
        def new_timed():
            """ Формирование новой контрольной суммы """
            castrol = 1
            for iterate in range(2 ** 10):
                castrol *= random.randrange(2 ** 5, 2 ** 80)
            return castrol
        # <<< Получение времени >>>
        hms = datetime.datetime.today()
        get_date = f"{hms.day}_{hms.month}_{hms.year}"
        get_time = f"{hms.hour}-{hms.minute}-{hms.second}"
        timed = new_timed()
        name_enc_folder = f"{get_date}_{get_time}/"

        def print_progress(type_work, current, total):
            cols = get_size_of_terminal()
            try:
                progress_status = ((current * 100) // total)
                to_print = ''
                if type_work == 'files':
                    to_print = 'Work completed on'
                elif type_work == 'folders':
                    to_print = 'Folder creation status'
                template_some_message(YELLOW, f"{to_print} {progress_status}% ({current}/{total})")
            except ZeroDivisionError:
                pass

        def encrypt_it(byte_file, key, iv):
            cfb_cipher = AES.new(key, AES.MODE_OFB, iv)
            return cfb_cipher.encrypt(byte_file)

        def decrypt_it(byte_file, key, iv):
            cfb_decipher = AES.new(key, AES.MODE_OFB, iv)
            return cfb_decipher.decrypt(byte_file)

        def read_bin_file(directory):
            file_to_read = open(directory, "rb")
            data = file_to_read.read()
            file_to_read.close()
            return data

        def write_bin_file(directory, data):
            file_to_write = open(directory, "wb")
            file_to_write.write(data)
            file_to_write.close()

        if os.path.exists(FOLDER_WITH_ENC_DATA) is False:
            os.system('mkdir ' + FOLDER_WITH_ENC_DATA)

        def template_not_confirmed(remove):
            os.chdir('../../')
            write_log('Not confirm', 'ALERT')
            template_some_message(RED, "** DA DUMM BASS **")
            sleep(5)
            if remove:
                template_remove_folder(FOLDER_WITH_DATA)
            quit()

        xzibit_hash_from_file = open(FILE_WITH_HASH_GENERIC_KEY).readline()
        check_generic_hash = check_password_hash(xzibit_hash_from_file, self.xzibit)
        if check_generic_hash is False:
            print(True)
            template_not_confirmed(True)
        else:
            if self.type_work == 'enc':
                def save_keyiv(key, file):
                    file_key = open(file, mode="wb")
                    keyiv = enc_keyiv(key, self.xzibit)
                    file_key.write(keyiv)
                    file_key.close()

                    key_data = read_bin_file(file)
                    write_bin_file(file, key_data)

                system_action('mkdir ' + FOLDER_FOR_ENCRYPTION_FILES)

                template_some_message(BLUE, " The program allows you to encrypt files")
                template_some_message(YELLOW, " - Please put the files you want to encrypt in \'FOR_ENCRYPTION\'")

                temp = input("Press \'Enter\' key to continue...")

                print("Generating KEY and IV for the recipient")
                key = Crypto.Random.new().read(AES.block_size)
                iv = Crypto.Random.new().read(AES.block_size)

                os.chdir(FOLDER_FOR_ENCRYPTION_FILES)

                if os.path.exists(name_enc_folder) is False:
                    system_action('mkdir ../' + name_enc_folder)

                path_to_key = '../' + name_enc_folder + KEY_FILE
                path_to_iv = '../' + name_enc_folder + IV_FILE
                path_to_signed = '../' + name_enc_folder + SIGNED
                path_to_timed = '../' + name_enc_folder + FILE_CONTROL_SUM

                template_some_message(YELLOW, "Beginning Encryption...\n")

                total_progress = progress = 0
                for i in os.walk('.'):
                    total_progress += 1
                for i in os.walk('.'):
                    try:
                        if os.path.exists('../' + name_enc_folder + i[0][2:]):
                            pass
                        else:
                            progress += 1
                            os.system('mkdir ../' + name_enc_folder + i[0][2:])
                            system_action('clear')
                            print_progress('folders', progress, total_progress)
                    except FileNotFoundError:
                        pass

                total_progress = progress = 0
                for root, dirs, files in os.walk('.', topdown=False):
                    for name in files:
                        total_progress += 1
                if total_progress != 0:
                    for root, dirs, files in os.walk('.', topdown=False):
                        for name in files:
                            progress += 1
                            file = os.path.join(root, name)
                            file = file[2:]
                            file_data = read_bin_file(file)
                            try:
                                write_bin_file('../' + name_enc_folder + file + ".elba", encrypt_it(file_data, key, iv))
                                system_action('clear')
                                print_progress('files', progress, total_progress)
                            except FileNotFoundError:
                                template_some_message(RED,
                                                      'Error in encryption file: directory must not contain a SPACE')
                                write_log('Directory has got space', 'FAIL')
                                quit()
                    save_keyiv(key, path_to_key)
                    save_keyiv(iv, path_to_iv)
                    control_sum = str(timed) + self.xzibit + str(timed)
                    enc_aes(path_to_timed, control_sum, self.xzibit)
                    with open(path_to_signed, 'w') as signature:
                        sign_xzibit = generate_password_hash(control_sum)
                        signature.write(sign_xzibit)
                        signature.close()
                    template_some_message(GREEN, "Encryption successful \n")
                    os.chdir('../../../')
                    write_log('Encryption successful', 'OK')
                else:
                    system_action('clear')
                    template_some_message(YELLOW, 'Empty directory')
                    os.chdir('../../../')
                    write_log('Empty directory', 'PASS')
                template_remove_folder(FOLDER_FOR_ENCRYPTION_FILES)
                sleep(2)

            elif self.type_work == 'dec':
                cnt = 0
                for folder in os.listdir(FOLDER_WITH_ENC_DATA):
                    if folder[:4] != PREFIX_FOR_DEC_FILE:
                        cnt += 1
                        print(f"{cnt}.", folder)
                if cnt == 0:
                    print(YELLOW, " - No data encryption - ")
                change_folder = int(input(YELLOW + '\n - Select folder by number: ' + DEFAULT_COLOR))
                n_cnt = 0
                for need_folder in os.listdir(FOLDER_WITH_ENC_DATA):
                    if need_folder[:4] != PREFIX_FOR_DEC_FILE:
                        n_cnt += 1
                        if n_cnt == change_folder:
                            template_some_message(YELLOW, "Beginning Decryption...\n")
                            os.chdir(FOLDER_WITH_ENC_DATA)
                            path_to_sign = need_folder + '/' + SIGNED
                            path_to_timed = need_folder + '/' + FILE_CONTROL_SUM

                            cnt_files = 0
                            for root, dirs, files in os.walk(need_folder, topdown=False):
                                for name in files:
                                    cnt_files += 1

                            if cnt_files != 0:
                                if os.path.exists(path_to_sign):
                                    control_sum = dec_aes(path_to_timed, self.xzibit)
                                    signature = open(path_to_sign, 'r').readline()
                                    sign_xzibit = check_password_hash(signature, control_sum)
                                    if sign_xzibit:
                                        new_folder = PREFIX_FOR_DEC_FILE + need_folder
                                        if os.path.exists(new_folder) is False:
                                            os.mkdir(new_folder)

                                        for i in os.walk(need_folder):
                                            if os.path.exists(new_folder + i[0].replace(need_folder, '')):
                                                pass
                                            else:
                                                os.system('mkdir ' + new_folder + i[0].replace(need_folder, ''))

                                        work_progress = 0
                                        for root, dirs, files in os.walk(need_folder, topdown=False):
                                            for name in files:
                                                work_progress += 1
                                                file = os.path.join(root, name)
                                                file = file.replace(need_folder + '/', '')

                                                enc_key = open(need_folder + '/' + KEY_FILE, 'rb').read()
                                                enc_iv = open(need_folder + '/' + IV_FILE, 'rb').read()

                                                key = dec_keyiv(enc_key, self.xzibit)
                                                iv = dec_keyiv(enc_iv, self.xzibit)

                                                if file.endswith('.elba'):
                                                    file_data = read_bin_file(need_folder + '/' + file)
                                                    write_bin_file(new_folder + '/' + file[:-5], decrypt_it(file_data, key, iv))
                                                system_action('clear')
                                                print_progress('files', work_progress-4, cnt_files-4)

                                        template_remove_folder(need_folder)
                                        os.chdir('../../')
                                        if cnt_files != 4:
                                            template_some_message(GREEN, "Decryption successful \n")
                                            write_log('Decryption successful', 'OK')
                                        sleep(1)
                                    else:
                                        template_not_confirmed(False)
                                else:
                                    template_not_confirmed(False)
                            else:
                                os.chdir('../../')
                                system_action('clear')
                                template_some_message(YELLOW, 'Empty directory')
                                sleep(2)


def actions_with_encryption_files(xzibit):
    system_action('clear')
    template_some_message(BLUE, "-- Go to the VOLARE/ENCRYPTION_DATA data folder and follow the instructions --")
    print(BLUE, f"1.{YELLOW} - Encryption files", DEFAULT_COLOR)
    print(BLUE, f"2.{YELLOW} - Decryption files", DEFAULT_COLOR)
    print(BLUE, "\n Press \'Enter\' to exit from encryption", DEFAULT_COLOR)
    change_action = input(YELLOW + "\n - Select by number: " + DEFAULT_COLOR)
    if change_action == '1':
        system_action('clear')
        system_action('file_manager')
        write_log("Try encryption", "RUN")
        WorkWithUserFiles(xzibit, 'enc').file_encryption_control()
    elif change_action == '2':
        system_action('clear')
        write_log("Try decryption", "RUN")
        WorkWithUserFiles(xzibit, 'dec').file_encryption_control()
    write_log("Exit from encrypt", "OK")
