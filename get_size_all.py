from enc_obs import *
from random import choice


symbols = 'd9webjv23jfjwq0pfk-0scl-0saas'

for i in range(1, 10000):
    massge = ''
    for j in range(16):
        massge += choice(symbols)
    message = enc_only_base64(massge, "kozak")
    for item in message:
        if item == '/':
            print(message)
