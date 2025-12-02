import numpy as np
from ciphertext import undigitize, is_valid, get_dictionary


def shift_encrypt(plaintext: np.ndarray, key: int) -> np.ndarray:
    """
    performs a shift cipher encryption by c = (p + key)%26

    Arguments
    ---------
    plaintext: the iterable of integers
    key: the shift amount

    Returns
    -------
    the ciphertext
    """
    return (plaintext + key)%26

def shift_decrypt(ciphertext: np.ndarray, key: int) -> np.ndarray:
    """
    performs a shift cipher decryption by c = (p - key)%26

    Arguments
    ---------
    ciphertext: the iterable of integers
    key: the de-shift amount

    Returns
    -------
    the plaintext
    """
    plaintext = shift_encrypt(ciphertext, -key)
    return plaintext

def shift_decrypt_exhaustive(ciphertext: np.ndarray) -> tuple[np.ndarray, int]|None:
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
    dictionary, max_word_len = get_dictionary('./dictionary.txt')
    for key in range(26):
        message = shift_decrypt(ciphertext, key)
        alpha_text = undigitize(message, 'plain')
        if is_valid(alpha_text, dictionary, max_word_len):
            return message, key
