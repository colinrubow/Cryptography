from math import gcd, sqrt
from mod_algebra import *
from utils import get_common_digrams, get_digram_counts
from ciphertext import digitize, undigitize
import os


def hill_encrypt(plaintext: list[int], key: list[list[int]]) -> list[int]:
    """
    performs a hill encryption by y = plaintext@key

    Arguments
    ---------
    plaintext: the message
    key: the linear transormation key

    Returns
    -------
    the ciphertext
    """
    m = len(key)
    # test if key is valid
    key_det = det(key)
    if key_det == 0 or gcd(key_det, 26) != 1:
        raise ValueError("key is non-invertible")
    # pad
    r = len(plaintext)%m
    if r != 0:
        plaintext += [1]*(m - r)
    ciphertext = []
    for i in range(0, len(plaintext), m):
        c = mult([plaintext[i:i+m]], key)
        ciphertext += c[0]
    return ciphertext

def hill_decrypt(ciphertext: list[int], key: list[list[int]]) -> list[int]:
    """
    performs a hill decryption by plaintext = y@key^(-1)

    Arguments
    ---------
    ciphertext: the message
    key: the linear transformation key

    Returns
    -------
    the plaintext
    """
    m = len(key)
    k_inv = inv(key)
    plaintext = []
    for i in range(0, len(ciphertext), m):
        p = mult([ciphertext[i:i+m]], k_inv)
        plaintext += p[0]
    return plaintext

def hill_decrypt_known_plaintext(plaintext: list[int], ciphertext: list[int]) -> list[list[int]]:
    """
    determines the key to a known plaintext hill cipher.

    Arguments
    ---------
    plaintext: duh
    ciphertext: duh

    Returns
    -------
    the key, a matrix
    """
    # get all potential key lengths
    ms = []
    for i in range(2, int(sqrt(len(plaintext))) + 1):
        if len(plaintext)%i == 0:
            ms.append(i)

    key = [[0]]
    solved = False
    for m in ms:
        # make the plaintext matrix
        x = [plaintext[i*m:(i+1)*m] for i in range(m)]

        # check if invertible
        # NOTE: if not invertible, will have to build the x matrix from other parts
        det_x = det(x)

        if det_x != 0 and gcd(det_x, 26) == 1:
            # make the ciphertext matrix
            y = [ciphertext[i*m:(i+1)*m] for i in range(m)]

            x_inv = inv(x)

            key = mult(x_inv, y)

            # check if we can encrypt the plaintext into the given ciphertext
            if hill_encrypt(plaintext, key) == ciphertext:
                solved = True
                break
    if solved:
            return key
    else:
        return [[0]]

def hill_decrypt_common_patterns(ciphertext: list[int]) -> tuple[list[int], list[list[int]]]:
    """
    determines the key and plaintext of a given ciphertext by assuming the most commmon digram or trigrams or etc correspond to the common patterns of english

    Arguments
    ---------
    ciphertext: the message

    Returns
    -------
    the plaintext, the key
    """
    common_digrams = get_common_digrams()

    digrams, _ = get_digram_counts(undigitize(ciphertext, 'cipher'))

    while True:
        os.system('cls')
        print('Common Digrams:\n')
        print(common_digrams)
        print()
        print('Digrams:\n')
        print(digrams)
        print()

        first_digram = input('First Cipher Diagram: ')
        second_digram = input('Second Cipher Digram: ')
        first_c_digram = input('First Common Digram: ')
        second_c_digram = input('Second Common Digram: ')

        dplaintext = digitize(first_c_digram) + digitize(second_c_digram)
        dciphertext = digitize(first_digram) + digitize(second_digram)

        try:
            key = hill_decrypt_known_plaintext(dplaintext, dciphertext)
        except:
            continue
        if key != [[0]]:
            dplaintext = hill_decrypt(ciphertext, key)
            plaintext = undigitize(dplaintext, 'plain')
            print(plaintext)
            correct = input('Correct (0/1)?: ')
            if correct == '0':
                continue
            else:
                break

    return dplaintext, key

if __name__ == '__main__':
    plaintext = 'july'
    dplaintext = digitize(plaintext)
    k = [[11, 8], [3, 7]]
    dciphertext = hill_encrypt(dplaintext, k)
    ciphertext = undigitize(dciphertext, 'cipher')
    assert ciphertext == 'DELW'

    dplaintext = hill_decrypt(dciphertext, k)
    plaintext = undigitize(dplaintext, 'plain')
    assert plaintext == 'july'

    plaintext = 'friday'
    dplaintext = digitize(plaintext)
    ciphertext = 'PQCFKU'
    dciphertext = digitize(ciphertext)
    k = hill_decrypt_known_plaintext(dplaintext, dciphertext)
    assert k == [[7, 19], [8, 3]]

    plaintext = 'breathtaking'
    dplaintext = digitize(plaintext)
    ciphertext = 'RUPOTENTOIFV'
    dciphertext = digitize(ciphertext)
    k = hill_decrypt_known_plaintext(dplaintext, dciphertext)
    assert undigitize(hill_encrypt(dplaintext, k), 'cipher') == ciphertext
    assert undigitize(hill_decrypt(dciphertext, k), 'plain') == plaintext

    ciphertext = 'LMQETXYEAGTXCTUIEWNCTXLZEWUAISPZYVAPEWLMGQWYAXFTCJMSQCADAGTXLMDXNXSNPJQSYVAPRIQSMHNOCVAXFV'
    dciphertext = digitize(ciphertext)
    dplaintext, k = hill_decrypt_common_patterns(dciphertext)
    plaintext = undigitize(dplaintext, 'plain')
    print(plaintext)
