import numpy as np
from typing import Callable


def shift_encrypt(plaintext: np.ndarray, key: int) -> np.ndarray:
    """
    performs a shift cipher encryption by c = (p + key)%27

    Arguments
    ---------
    plaintext: the iterable of integers
    key: the shift amount

    Returns
    -------
    the ciphertext
    """
    return (plaintext + key)%27

def shift_decrypt_exhaustive(ciphertext: np.ndarray, is_valid: Callable) -> tuple[np.ndarray, int]|None:
    """
    decrypts the shift cipher by exhaustive search from key = 0 to 26

    Arguments
    ---------
    ciphertext: the code to break
    is_valid: a test to determine if the deciphered code is valid

    Returns
    -------
    the plaintext with the key or None if no solution found
    """
    for key in range(27):
        message = (ciphertext - key)%27
        if is_valid(message):
            return message, key
