from permutation_cipher import permute_encrypt
from ciphertext import *

plaintext = 'iknowyourdreamsyoufoolishgirl'
ciphertext = permute_encrypt(list(plaintext), [2,0,1])
print(ciphertext)
