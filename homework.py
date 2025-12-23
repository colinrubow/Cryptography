from vigenere_cipher import vigenere_decrypt_kasiski_index
from ciphertext import *

ciphertext = read('./exercises/Chapter_01/1_21d.txt', 'cipher')
dciphertext = digitize(ciphertext)
dplaintext, key = vigenere_decrypt_kasiski_index(dciphertext, 'index')

print(undigitize(key, 'cipher'))
print(undigitize(dplaintext, 'plain'))
