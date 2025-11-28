from shift_cipher import shift_decrypt_exhaustive
from ciphertext import *

ciphertext = read('./exercises/Chapter_01/1_5.txt', 'cipher')
dciphertext = digitize(ciphertext)
result = shift_decrypt_exhaustive(dciphertext)
if result is not None:
    key = result[1]
    plaintext = undigitize(result[0], 'plain')
    print(key, plaintext)
else:
    print('no decryption found')
