from base64 import urlsafe_b64encode, urlsafe_b64decode
import base64
import hashlib
import random
import os

from stdiomask import getpass
from werkzeug.security import check_password_hash, generate_password_hash

from Crypto.Cipher import AES
import Crypto.Random

from main import *


__version__ = '2.0.2'


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


def save_data_to_file(data_1, data_2, data_3, master_password, type_data):

    def path_to_data_to_save_resource(enc_name_type_folder):
        return FOLDER_WITH_RESOURCES + enc_name_type_folder

    def path_to_data_to_save_note(enc_name_type_folder):
        return FOLDER_WITH_NOTES + enc_name_type_folder

    enc_name_resource_folder = enc_only_base64(data_1, master_password) + '/'    # Шифрование папки с названием
    enc_name_note_folder = enc_only_base64(data_1, master_password) + '/'

    if os.path.exists(path_to_data_to_save_resource(enc_name_resource_folder)) is False:
        os.mkdir(path_to_data_to_save_resource(enc_name_resource_folder))

    if os.path.exists(path_to_data_to_save_note(enc_name_resource_folder)) is False:
        os.mkdir(path_to_data_to_save_note(enc_name_resource_folder))

    if type_data == 'resource':
        resource_folder = path_to_data_to_save_resource(enc_name_resource_folder)
        login_folder = path_to_data_to_save_resource(enc_name_resource_folder)
        password_folder = path_to_data_to_save_resource(enc_name_resource_folder)

        resource_file = resource_folder + FILE_RESOURCE
        login_file = login_folder + FILE_LOGIN
        password_file = password_folder + FILE_PASSWORD

        enc_aes(resource_file, data_1, master_password)
        enc_aes(login_file, data_2, master_password)
        enc_aes(password_file, data_3, master_password)

    if type_data == 'note':
        name_note = path_to_data_to_save_note(enc_name_note_folder)
        self_note = path_to_data_to_save_note(enc_name_note_folder)

        name_note_file = name_note + FILE_NOTE_NAME
        note_file = self_note + FILE_NOTE_ITSELF

        enc_aes(name_note_file, data_1, master_password)
        enc_aes(note_file, data_2, master_password)


def show_decryption_data(master_password, category):
    system_action('clear')
    print(PURPLE, "     ___________________________________")
    print(PURPLE, "    /\/| ", YELLOW, "\/                   \/", PURPLE, " |\/\ ")
    print(PURPLE, "   /\/\|", YELLOW, " \/  Saved " + category + 's' + "  \/ ", PURPLE, "|/\/\ ", DEFAULT_COLOR)
    print(YELLOW, "           \/                   \/ ", DEFAULT_COLOR)
    print('\n'*5)

    s = 0

    type_folder = ''
    if category == 'resource':
        type_folder = FOLDER_WITH_RESOURCES
    if category == 'note':
        type_folder = FOLDER_WITH_NOTES

    for category_item in os.listdir(type_folder):
        decryption_data = dec_only_base64(category_item, master_password)
        s += 1
        print(PURPLE, str(s) + '.', YELLOW, decryption_data, DEFAULT_COLOR)
    if category == 'resource':
        print(BLUE +
              '\n  - Enter "-r" to restart, "-x" to exit'
              '\n  - Enter "-a" to add new resource'
              '\n  - Enter "-c" to change master-password'
              '\n  - Enter "-d" to remove resource',
              BLUE,
              RED, '\n  - Enter "-n" to go to notes            !',
              BLUE,
              '\n  - Enter "-u" to update program'
              '\n  - Enter "-z" to remove ALL data',
              YELLOW,
              '\n Select resource by number \n', DEFAULT_COLOR)
    if category == 'note':
        print(BLUE + '\n  - Press "Enter" to go back'
                     '\n  - Enter "-a" to add new note'
                     '\n  - Enter "-d" to remove note',
              YELLOW, '\n Select note by number', DEFAULT_COLOR)
    if s == 0:
        print(YELLOW + '\n    No ' + category + 's' + ' saved \n')
