import numpy as np


def permute_encrypt(plaintext: np.ndarray, key: list[int]) -> np.ndarray:
    """
    encryptes the text by permuting every m=len(key) characters according to the key

    Arguments
    ---------
    plaintext: the message to encrypt
    key: a list mapping each index to its new position
    """
    m = len(key)
    plaintext + ['a']*(m - len(plaintext)%m)
