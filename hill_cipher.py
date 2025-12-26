from math import gcd, sqrt
from mod_algebra import *


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
    plaintext += [1]*(m - len(plaintext)%m)
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
    # test if key is valid (will raise exception if not)
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
                break
    return key
