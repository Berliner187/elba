import base64
from Crypto.Hash import SHA256, HMAC
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import os

ALGORITHM_NONCE_SIZE = 12
ALGORITHM_TAG_SIZE = 16
ALGORITHM_KEY_SIZE = 16
PBKDF2_SALT_SIZE = 16
PBKDF2_ITERATIONS = 32767
PBKDF2_LAMBDA = lambda x, y: HMAC.new(x, y, SHA256).digest()


def enc_mask_level(text, encoding='utf-8', errors='surrogatepass'):
    """ Translation to binary view """
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def dec_mask_level(bits, encoding='utf-8', errors='surrogatepass'):
    """ Translation from binary """
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def enc_with_only_base64(message, password):
    """ Base64-based encryption """
    enc = []
    for i in range(len(message)):
        key_c = password[i % len(password)]
        enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
    encryption = base64.urlsafe_b64encode("".join(enc).encode()).decode()
    return encryption


def dec_with_only_base64(encryption, password):
    """ Base64-based decryption """
    dec = []
    message = base64.urlsafe_b64decode(encryption).decode()
    for i in range(len(message)):
        key_c = password[i % len(password)]
        dec.append(chr((256 + ord(message[i]) - ord(key_c)) % 256))
    return "".join(dec)


def enc_with_AES(plaintext, password):
    # Generate a 128-bit salt using a CSPRNG.
    salt = get_random_bytes(PBKDF2_SALT_SIZE)
    # Derive a key using PBKDF2.
    key = PBKDF2(password, salt, ALGORITHM_KEY_SIZE, PBKDF2_ITERATIONS, PBKDF2_LAMBDA)
    # Encrypt and prepend salt.
    ciphertextAndNonce = enc_additional_for_AES(plaintext.encode('utf-8'), key)
    ciphertextAndNonceAndSalt = salt + ciphertextAndNonce
    # Return as base64 string.
    return base64.b64encode(ciphertextAndNonceAndSalt)


def dec_with_AES(base64CiphertextAndNonceAndSalt, password):
    # Decode the base64.
    ciphertextAndNonceAndSalt = base64.b64decode(base64CiphertextAndNonceAndSalt)
    # Get the salt and ciphertextAndNonce.
    salt = ciphertextAndNonceAndSalt[:PBKDF2_SALT_SIZE]
    ciphertextAndNonce = ciphertextAndNonceAndSalt[PBKDF2_SALT_SIZE:]
    # Derive the key using PBKDF2.
    key = PBKDF2(password, salt, ALGORITHM_KEY_SIZE, PBKDF2_ITERATIONS, PBKDF2_LAMBDA)
    # Decrypt and return result.
    plaintext = dec_additional_for_AES(ciphertextAndNonce, key)
    return plaintext.decode('utf-8')


def enc_additional_for_AES(plaintext, key):
    # Generate a 96-bit nonce using a CSPRNG.
    nonce = get_random_bytes(ALGORITHM_NONCE_SIZE)
    # Create the cipher.
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    # Encrypt and prepend nonce.
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    ciphertextAndNonce = nonce + ciphertext + tag
    return ciphertextAndNonce


def dec_additional_for_AES(ciphertextAndNonce, key):
    # Get the nonce, ciphertext and tag.
    nonce = ciphertextAndNonce[:ALGORITHM_NONCE_SIZE]
    ciphertext = ciphertextAndNonce[ALGORITHM_NONCE_SIZE:len(ciphertextAndNonce) - ALGORITHM_TAG_SIZE]
    tag = ciphertextAndNonce[len(ciphertextAndNonce) - ALGORITHM_TAG_SIZE:]
    # Create the cipher.
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    # Decrypt and return result.
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext


def enc_data(anything, master_password):   # Encryption by two levels
    crypto_1 = enc_with_AES(anything, master_password)
    # crypto_2 = enc_with_only_base64(crypto_1, master_password)
    # total = enc_mask_level(str(crypto_1))
    return crypto_1


def dec_data(anything, master_password):   # Decryption by two levels
    # decryption_1 = dec_mask_level(anything)
    # decryption_2 = dec_with_only_base64(anything, master_password)
    total = dec_with_AES(anything, master_password)
    return total


from csv import DictWriter, DictReader

password = 'password'
__enc__ = enc_data('password', password)

file_dat = 'enc_data.dat'
file_csv = 'enc_data.csv'

# if os.path.exists(file_csv) == bool(False):
#     with open(file_csv, 'wb') as encryption:
#         writer = DictWriter(encryption, fieldnames=['col_1', 'col_2', 'col_3'])
#         writer.writeheader()
#         writer.writerow({
#             'col_1': 'resource',
#             'col_2': 'login',
#             'col_3': __enc__
#         })
#
# else:
#     with open(file_csv, 'rb') as from_file:
#         reader = DictReader(from_file)
#         for item in reader:
#             decryption = dec_data(item['col_3'], password)
#             print(decryption)

if os.path.exists(file_dat) == bool(False):
    with open(file_dat, 'wb') as file:
        file.write(__enc__)
        file.close()
else:
    with open(file_dat, 'rb') as from_file:
        enc_from_file = from_file.readline()
        print(enc_from_file)
        __dec__ = dec_data(enc_from_file, password)
        print(__dec__)
        from_file.close()
