from ciphertext import undigitize, is_valid
from utils import get_dictionary, index_of_coincidence


def shift_encrypt(plaintext: list[int], key: int) -> list[int]:
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
    return [(p + key)%26 for p in plaintext]

def shift_decrypt(ciphertext: list[int], key: int) -> list[int]:
    """
    performs a shift cipher decryption by p = (c - key)%26

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

def shift_decrypt_exhaustive(ciphertext: list[int]) -> tuple[list[int], int]|None:
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
        if is_valid(alpha_text, dictionary, max_word_len, min_req_score=10):
            return message, key
