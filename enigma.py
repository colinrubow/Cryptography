from utils import get_dictionary
from ciphertext import is_valid, undigitize


def enigma_encrypt(plaintext: list[int], pi: dict[int, int], key: int) -> list[int]:
    """
    performs this engimaesque encryption by first running the plaintext through the permutation (pi), then adding it to the keystream. This is done by pi(x) + (key + i - 1)mod26

    Arguments
    ---------
    plaintext: the message
    pi: the permutation in Z26
    key: the keystream key

    Returns
    -------
    the ciphertext
    """
    ciphertext = plaintext.copy()
    for i in range(len(ciphertext)):
        ciphertext[i] = (pi[ciphertext[i]] + key + i - 1)%26
    return ciphertext

def enigma_decrypt(ciphertext: list[int], pi: dict[int, int], key: int) -> list[int]:
    """
    decrypts the enigmaesque by pi^{-1}(y - (key + i - 1))%26

    Arguments
    ---------
    ciphertext: the message
    pi: the permutation
    key: the keystream key

    Returns
    -------
    the plaintext
    """
    plaintext = ciphertext.copy()
    pi_inv = {v:k for k, v in pi.items()}
    for i in range(len(plaintext)):
        plaintext[i] = pi_inv[(plaintext[i] - (key + i - 1))%26]
    return plaintext

def enigma_known_perm_decrypt_exhaustive(ciphertext: list[int], pi: dict[int, int]) -> tuple[list[int], int]|None:
    """
    decrypts by exhaustion a known permutation.

    Arguments
    ---------
    ciphertext: the message
    pi: the permutation

    Returns
    -------
    the message and the key or None if no solution found
    """
    dictionary, max_word_len = get_dictionary('./dictionary.txt')
    for key in range(26):
        message = enigma_decrypt(ciphertext, pi, key)
        alpha_text = undigitize(message, 'plain')
        if is_valid(alpha_text, dictionary, max_word_len, min_req_score=10):
            return message, key
