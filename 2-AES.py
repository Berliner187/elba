#!/usr/bin/env python3
import base64
import hashlib
import random
import os
from csv import DictReader, DictWriter
from werkzeug.security import check_password_hash, generate_password_hash

from Crypto.Cipher import AES
import Crypto.Random


class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Crypto.Random.new().read(AES.block_size)
        #                    | here is the difference to the iv from decrypt
        # iv = b'\xe2\xe0l3H\xc42*N\xb0\x152\x98\x9cBh'
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        code = cipher.encrypt((raw.encode()))
        return base64.b64encode(iv + code)

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        #                    | here is the difference to the iv from encrypt
        # iv = b'\xe2\xe0l3H\xc52*N\xb0\x152\x98\x9cBh'
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


def gen_key():
    lister = 'zxcvbnmasdfghjklqwertyuiop1234567890'
    key = ''
    for i in range(16):
        key += random.choice(lister)
    return key


if __name__ == '__main__':
    message = "Security"

    __file__ = 'data.csv'
    __hash__ = 'hash.dat'

    __key__ = 'zxcvbnmasdfghjklqwertyuiop1234567890'

    if os.path.exists(__file__) == bool(False):

        hash_to_file = generate_password_hash(__key__)
        with open(__hash__, 'w') as hash_pas:
            hash_pas.write(hash_to_file)
            hash_pas.close()

        with open(__file__, 'w') as headers:
            writer = DictWriter(headers, fieldnames=['key', 'value'])
            writer.writeheader()

        with open(__file__, 'w') as enc_data:
            writer = DictWriter(enc_data, fieldnames=['key', 'value'])
            aes = AESCipher(__key__)
            payload = aes.encrypt(message)
            print(payload)
            writer.writerow({
                'key': 'key',
                'value': bytes(payload)
            })
            print('OK')

    else:
        with open(__hash__, 'r') as load_hash:
            hash_password = check_password_hash(load_hash.readline(), __key__)
            load_hash.close()

        if hash_password:
            # with open(__file__, 'ab') as enc_data:
            #     writer = DictWriter(enc_data, fieldnames=['key', 'value'])
            #     aes = AESCipher(__key__)
            #     payload = aes.encrypt(message)
            #     writer.writerow({
            #         'key': 'add key',
            #         'value': bytes(payload)
            #     })

            with open(__file__, 'rb') as read_file:
                reader = DictReader(read_file)
                for item in reader:
                    aes = AESCipher(__key__)
                    print('Decryption:', bytes(aes.decrypt(item['value'])))
        else:
            print('\n --- Wrong password --- ')
