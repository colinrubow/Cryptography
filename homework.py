from permutation_cipher import permute_decrypt
from ciphertext import *

ciphertext = read('./exercises/Chapter_01/1_16b.txt', 'cipher')
dciphertext = digitize(ciphertext)
key = [4, 1, 6, 2, 7, 3, 8, 5]
key = [k - 1 for k in key]
result = permute_decrypt(dciphertext, key)
result = undigitize(result, 'cipher')
print(result)
