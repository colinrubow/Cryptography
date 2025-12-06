import numpy as np
from ciphertext import digitize, is_valid, undigitize
from utils import get_common_letters, get_dictionary, get_letter_counts


def affine_encrypt(plaintext: np.ndarray, key: tuple[int, int]) -> np.ndarray:
    """
    performs an affine encryption by c = (key[0]*p + key[1])%26

    Arguments
    ---------
    plaintext: the message to encrypt
    key: the first term is the multiplication and the second is the addition

    Returns
    -------
    the ciphertext
    """
    if np.gcd(key[0], 26) > 1:
        raise ValueError(f'The key is invalid. gcd({key[0]}, 26) != 1')
    return (plaintext*key[0] + key[1])%26

def affine_decrypt(ciphertext: np.ndarray, key: tuple[int, int]) -> np.ndarray:
    """
    performs an affine decryption by p = key[0]^-1(c - key[1])%26

    Arguments
    ---------
    ciphertext: the message to decrypt
    key: the first term is the multiplication and the second is the addition

    Returns
    -------
    the plaintext
    """
    if np.gcd(key[0], 26) > 1:
        raise ValueError(f'The key is invalid. gcd({key[0]}, 26) != 1')
    a_inverse = pow(key[0], -1, 26)
    return (a_inverse * (ciphertext - key[1]))%26

def affine_decrypt_frequency(ciphertext: np.ndarray) -> tuple[np.ndarray, tuple[int, int]]|None:
    """
    performs decryption by solving the system of two linear equations given by the two most frequent letters

    Arguments
    ---------
    ciphertext: the message

    Returns
    -------
    the decrypted message along with the key or None if no solution is found
    """
    # FIXME: doesn't workuuuuh
    dictionary, max_word_len = get_dictionary('./dictionary.txt')

    tciphertext = undigitize(ciphertext, 'cipher')
    letters, _ = get_letter_counts(tciphertext)
    common_letters = get_common_letters()
    for i, letter_1 in enumerate(letters):
        cipher_1 = int(digitize(letter_1)[0])
        plain_1 = int(digitize(common_letters[i])[0])
        for j, letter_2 in enumerate(letters[i+1:]):
            cipher_2 = int(digitize(letter_2)[0])
            plain_2 = int(digitize(common_letters[i+j+1])[0])

            delta_p = (plain_1 - plain_2) % 26
            if np.gcd(delta_p, 26) == 1:
                a = ((cipher_1 - cipher_2) * pow(delta_p, -1, 26)) % 26
                b = (cipher_1 - a * plain_1) % 26
                if np.gcd(a, 26) == 1:
                    plaintext = affine_decrypt(ciphertext, (a, b))
                    tplaintext = undigitize(plaintext, 'plain')
                    print(tplaintext)
                    if is_valid(tplaintext, dictionary, max_word_len):
                        return plaintext, (a, b)
