from mod_algebra import *
from math import gcd, sqrt


def affine_hill_encrypt(plaintext: list[int], key: tuple[list[list[int]], list[int]]) -> list[int]:
    """
    performs an affine hill encryption by y = plaintext@key[0] + key[1]

    Arguments
    ---------
    plaintext: the message
    key: the first is the matrix, the second is the shift b

    Returns
    -------
    the ciphertext
    """
    k_m, k_b = key
    m = len(k_m)
    # test if key is valid
    k_m_det = det(k_m)
    if k_m_det == 0 or gcd(k_m_det, 26) != 1:
        raise ValueError('key is non-invertible')
    # pad
    plaintext += [1]*(m - len(plaintext)%m)
    ciphertext = []
    for i in range(0, len(plaintext), m):
        c = mult([plaintext[i:i+m]], k_m)[0]
        c = [num + num_b for num, num_b in zip(c, k_b)]
        ciphertext += c
    return ciphertext

def affine_hill_decrypt(ciphertext: list[int], key: tuple[list[list[int]], list[int]]) -> list[int]:
    """
    performs an affine hill decryption by x = (ciphertext - key[1])@key[0]^{-1}

    Arguments
    ---------
    ciphertext: the message
    key: the first is the matrix, the second is the shift b

    Returns
    -------
    the plaintext
    """
    k_m, k_b = key
    m = len(k_m)
    k_m_inv = inv(k_m)
    plaintext = []
    for i in range(0, len(ciphertext), m):
        p = [num - num_b for num, num_b in zip(ciphertext[i:i+m], k_b)]
        p = mult([p], k_m_inv)
        plaintext += p[0]
    return plaintext

def affine_hill_decrypt_known_plaintext(plaintext: list[int], ciphertext: list[int]) -> tuple[list[list[int]], list[int]]:
    """
    determines the key to a known plaintext affine hill cipher

    Arguments
    ---------
    plaintext: duh
    ciphertext: duh

    Returns
    -------
    the key, the matrix and the shift
    """
    # get all potential key lengths
    ms = []
    for i in range(2, int(sqrt(len(plaintext)/2)) + 1):
        if len(plaintext)%i == 0:
            ms.append(i)

    k_m = [[0]]
    k_b = [0]
    for m in ms:
        # make the plaintext matrices
        x_1 = [plaintext[i*m:(i+1)*m] for i in range(m)]
        x_2 = [plaintext[i*m:(i+1)*m] for i in range(m, 2*m)]

        # check if invertible
        x_sub = sub(x_1, x_2)
        det_x = det(x_sub)

        if det_x != 0 and gcd(det_x, 26) == 1:
            # make the ciphertext matrices
            y_1 = [ciphertext[i*m:(i+1)*m] for i in range(m)]
            y_2 = [ciphertext[i*m:(i+1)*m] for i in range(m, 2*m)]

            x_inv = inv(x_sub)

            k_m = mult(sub(y_1, y_2), x_inv)

            k_b = sub(y_1, mult(x_1, k_m))[0]

            # check if we can ecrypt the plaintext into the given ciphertext
            if affine_hill_encrypt(plaintext, (k_m, k_b)) == ciphertext:
                break
    return k_m, k_b
