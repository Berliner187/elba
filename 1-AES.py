import base64
import hashlib
import random
import os
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
    message = "Confidence information"

    __file__ = 'data.dat'
    __hash__ = 'hash.dat'

    __key__ = input(' - Password: ')  # 'zxcvbnmasdfghjklqwertyuiop1234567890'

    if os.path.exists(__file__) == bool(False):
        hash_to_file = generate_password_hash(__key__)
        with open(__hash__, 'w') as hash_pas:
            hash_pas.write(hash_to_file)
            hash_pas.close()

        with open(__file__, 'wb') as enc_data:
            aes = AESCipher(__key__)
            payload = aes.encrypt(message)
            enc_data.write(payload)
            enc_data.close()
            print(payload)

        with open(__file__, 'a') as write_space:
            write_space.write('\n')
            write_space.close()

    else:
        with open(__hash__, 'r') as load_hash:
            hash_password = check_password_hash(load_hash.readline(), __key__)
            load_hash.close()

        if hash_password:
            with open(__file__, 'ab') as enc_data:
                aes = AESCipher(__key__)
                payload = aes.encrypt(message)
                enc_data.write(payload)
                enc_data.close()

            with open(__file__, 'a') as write_space:
                write_space.write('\n')
                write_space.close()

            with open(__file__, 'rb') as read_file:
                payload = read_file.readlines()
                for item in payload:
                    aes = AESCipher(__key__)
                    print('Decryption:', aes.decrypt(item))
        else:
            print('\n --- Wrong password --- ')
