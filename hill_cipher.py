from numpy import array
from numpy.linalg import inv, det
from math import gcd


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
    k = array(key, dtype=int)
    # test if key is valid
    if det(k) == 0 or gcd(det(k), 26) != 1:
        raise ValueError(f'invalid key has determinent {det(k)}')
    # pad
    plaintext += [1]*(m - len(plaintext)%m)
    ciphertext = []
    for i in range(0, len(plaintext), m):
        c = plaintext[i:i+m]@k
        for t in c:
            ciphertext.append(int(t))
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
    k = array(key)
    # test if key is valid
    if det(k) == 0 or gcd(det(k), 26) != 1:
        raise ValueError(f'invalid key has determinent {det(k)}')
    k_inv = inv(k)
    plaintext = []
    for i in range(0, len(ciphertext), m):
        p = ciphertext[i:i+m]@k_inv
        for t in p:
            plaintext.append(int(t))
    return plaintext
