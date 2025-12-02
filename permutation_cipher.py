import numpy as np


def permute_encrypt(plaintext: np.ndarray, key: list[int]) -> np.ndarray:
    """
    encryptes the text by permuting every m=len(key) characters according to the key

    Arguments
    ---------
    plaintext: the message to encrypt
    key: a list mapping each index to its new position

    Returns
    -------
    the ciphertext
    """
    m = len(key)
    # pad the edge
    edge = len(plaintext)%m
    if edge != 0:
        ciphertext = np.hstack((plaintext, ['0']*(m - edge)))
    else:
        ciphertext = plaintext.copy()

    for i in range(0, len(ciphertext), m):
        ciphertext[i:i+m] = [ciphertext[i:i+m][k] for k in key]
    return ciphertext

def permute_decrypt(ciphertext: np.ndarray, key: list[int]) -> np.ndarray:
    """
    decrypts the text by permuting every m=len(key) characters according to the inverse permuation of the key

    Arguments
    ---------
    ciphertext: the message to decrypt
    key: a list mapping each index to its new position

    Returns
    -------
    the plaintext
    """
    m = len(key)
    if len(ciphertext)%m != 0:
        raise ValueError('the ciphertext was not encrypted with this key as there was not put padding on the ciphertext')

    # find the inverse key
    new_key = []
    for i in range(m):
        new_key.append(key.index(i))

    plaintext = permute_encrypt(ciphertext, new_key)
    return plaintext
