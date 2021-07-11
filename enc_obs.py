# -*- encryption: UTF-8 -*-
from base64 import urlsafe_b64encode, urlsafe_b64decode
import base64
import hashlib
import random
import os
from time import sleep
import datetime


try:
    from stdiomask import getpass
    from werkzeug.security import check_password_hash, generate_password_hash
    from Crypto.Cipher import AES
    import Crypto.Random
except ModuleNotFoundError as error_module:
    write_log(error_module, 'CRASH')
    print(RED, 'Error: \n' + str(error_module), DEFAULT_COLOR)
    print('\n')
    template_some_message(
        YELLOW, "Please, install module/modules with PIP and restart the program"
    )
    quit()


from main import *


__version__ = '3.0.1'


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


def enc_binary(text, encoding='utf-8', errors='surrogatepass'):
    """ Translation to binary view """
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def dec_binary(bits, encoding='utf-8', errors='surrogatepass'):
    """ Translation from binary """
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


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


def enc_two_levels(anything, master_password):   # Encryption by two levels
    crypto_start = enc_base64(anything, master_password)
    crypto = enc_binary(crypto_start)
    return crypto


def dec_two_levels(anything, master_password):   # Decryption by two levels
    decryption_start = dec_binary(anything)
    decryption = dec_base64(decryption_start, master_password)
    return decryption


def enc_aes(__file__, encryption, __key__):
    with open(__file__, 'wb') as enc_data:
        aes = AESCipher(__key__)
        payload = aes.encrypt(encryption)
        enc_data.write(payload)
        enc_data.close()

    with open(__file__, 'a') as write_space:
        write_space.write('\n')
        write_space.close()


def dec_aes(__file__, __key__):
    with open(__file__, 'rb') as read_file:
        payload = read_file.readlines()
        for item in payload:
            aes = AESCipher(__key__)
            return aes.decrypt(item)


def enc_keyiv(keyiv, generic_key):
    aes = AESCipher(generic_key)
    return aes.encrypt(keyiv)


def dec_keyiv(enc_keyiv, generic_key):
    aes = AESCipher(generic_key)
    return aes.decrypt(enc_keyiv)


def save_data_to_file(data_1, data_2, data_3, generic_key, type_data):

    def path_to_data_to_save_resource(enc_name_type_folder):
        return FOLDER_WITH_RESOURCES + enc_name_type_folder

    def path_to_data_to_save_note(enc_name_type_folder):
        return FOLDER_WITH_NOTES + enc_name_type_folder

    if type_data == 'resource':
        enc_name_resource_folder = enc_only_base64(data_1, generic_key) + '/'
        if os.path.exists(path_to_data_to_save_resource(enc_name_resource_folder)) is False:
            os.mkdir(path_to_data_to_save_resource(enc_name_resource_folder))

        resource_folder = path_to_data_to_save_resource(enc_name_resource_folder)
        login_folder = path_to_data_to_save_resource(enc_name_resource_folder)
        password_folder = path_to_data_to_save_resource(enc_name_resource_folder)

        resource_file = resource_folder + FILE_RESOURCE
        login_file = login_folder + FILE_LOGIN
        password_file = password_folder + FILE_PASSWORD

        enc_aes(resource_file, data_1, generic_key)
        enc_aes(login_file, data_2, generic_key)
        enc_aes(password_file, data_3, generic_key)

    if type_data == 'note':
        enc_name_note_folder = enc_only_base64(data_1, generic_key) + '/'
        if os.path.exists(path_to_data_to_save_note(enc_name_note_folder)) is False:
            os.mkdir(path_to_data_to_save_note(enc_name_note_folder))

        name_note = path_to_data_to_save_note(enc_name_note_folder)
        self_note = path_to_data_to_save_note(enc_name_note_folder)

        name_note_file = name_note + FILE_NOTE_NAME
        note_file = self_note + FILE_NOTE_ITSELF

        enc_aes(name_note_file, data_1, generic_key)
        enc_aes(note_file, data_2, generic_key)


class WorkWithUserFiles:
    def __init__(self, generic_key, type_work):
        self.generic_key = generic_key
        self.type_work = type_work

    def file_encryption_control(self):
        FOLDER_WITH_ENC_DATA = FOLDER_WITH_DATA + 'ENCRYPTION_DATA/'
        FOLDER_FOR_ENCRYPTION_FILES = FOLDER_WITH_ENC_DATA + 'FOR_ENCRYPTION'
        # FOLDER_WITH_ENC_FILES = FOLDER_WITH_ENC_DATA + 'ENCRYPTED'
        PREFIX_FOR_DEC_FILE = '_DEC'

        hms = datetime.datetime.today()
        NAME_ENC_FOLDER = str(hms.hour * 3600 + hms.minute * 60 + hms.second + hms.day)
        FOLDER_WITH_ENC_FILES = FOLDER_WITH_ENC_DATA + NAME_ENC_FOLDER
        KEY_FILE = 'ONE.key'
        IV_FILE = 'TWO.key'

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

        if self.type_work == 'enc':
            def save_keyiv(key, file):
                file_key = open(file, "wb")
                file_key.write(key)
                file_key.close()

                key_data = read_bin_file(file)
                write_bin_file(file, key_data)

            system_action('mkdir ' + FOLDER_FOR_ENCRYPTION_FILES)

            print(BLUE, "\n The program allows you to encrypt files", DEFAULT_COLOR)
            print(YELLOW, "\n - Please put the files you want to encrypt in \'FOR_ENCRYPTION\'", DEFAULT_COLOR)

            temp = input("Press \'Enter\' key to continue...")

            if os.path.exists(FOLDER_WITH_ENC_FILES) is False:
                system_action('mkdir ' + FOLDER_WITH_ENC_FILES)
            key = Crypto.Random.new().read(AES.block_size)
            iv = Crypto.Random.new().read(AES.block_size)
            print("Generating KEY and IV for the recipient")

            path_to_key_one = FOLDER_WITH_ENC_FILES + '/' + NAME_ENC_FOLDER + KEY_FILE
            path_to_key_two = FOLDER_WITH_ENC_FILES + '/' + NAME_ENC_FOLDER + IV_FILE
            # else:
            #     key = read_bin_file(KEY_FILE)
            #     iv = read_bin_file(IV_FILE)
            #     print(key, iv)

            print("Beginning Encryption...\n")
            for file in os.listdir(FOLDER_FOR_ENCRYPTION_FILES):
                print("Encrypting", file)
                file_data = read_bin_file(FOLDER_FOR_ENCRYPTION_FILES + '/' + file)
                write_bin_file(FOLDER_WITH_ENC_FILES + '/' + file + ".elba", encrypt_it(file_data, key, iv))
                print("Completed encrypting", file, "\n")

            save_keyiv(key, path_to_key_one)
            save_keyiv(iv, path_to_key_two)

            print(GREEN + "Encryption successful\n" + DEFAULT_COLOR)
            template_remove_folder(FOLDER_FOR_ENCRYPTION_FILES)
            sleep(3)

        if self.type_work == 'dec':
            cnt = 0
            for folder in os.listdir(FOLDER_WITH_ENC_DATA):
                cnt += 1
                print(str(cnt) + '.', folder)
            change_folder = int(input(YELLOW + '\n - Select folder by number: ' + DEFAULT_COLOR))
            n_cnt = 0
            for need_folder in os.listdir(FOLDER_WITH_ENC_DATA):
                n_cnt += 1
                if n_cnt == change_folder:
                    for file in os.listdir(FOLDER_WITH_ENC_DATA + need_folder):
                        print("Decrypting", file)

                        new_folder = FOLDER_WITH_ENC_DATA + need_folder + PREFIX_FOR_DEC_FILE

                        if os.path.exists(new_folder) is False:
                            os.mkdir(new_folder)

                        key = open(FOLDER_WITH_ENC_DATA + need_folder + '/' + need_folder + KEY_FILE, 'rb').read()
                        iv = open(FOLDER_WITH_ENC_DATA + need_folder + '/' + need_folder + IV_FILE, 'rb').read()

                        if file.endswith('.elba'):
                            file_data = read_bin_file(
                                FOLDER_WITH_ENC_DATA + need_folder + '/' + file
                            )
                            write_bin_file(
                                new_folder + '/' + file[:-5],
                                decrypt_it(file_data, key, iv)
                            )

                            print(YELLOW, "Completed decrypting", DEFAULT_COLOR, file, "\n")
                    print(GREEN + "Decryption successful\n", DEFAULT_COLOR)
                    template_remove_folder(FOLDER_WITH_ENC_DATA + need_folder)
                    sleep(3)
