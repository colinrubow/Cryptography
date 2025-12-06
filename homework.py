from affine_cipher import affine_decrypt_frequency
from ciphertext import *

ciphertext = read('./exercises/Chapter_01/1_21c.txt', 'cipher')
dciphertext = digitize(ciphertext)
result = affine_decrypt_frequency(dciphertext)
if result is None:
    print('no solution')
else:
    plaintext = undigitize(result[0], 'plain')
    print(plaintext, result[1])
