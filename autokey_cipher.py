from ciphertext import undigitize, is_valid
import ciphertext
from utils import get_dictionary


def autokey_encrypt(plaintext: list[int], key: int) -> list[int]:
    """
    performs an autokey encryption by creating the keystream from the plaintext, starting from key

    Arguments
    ---------
    plaintext: the message
    key: the first number for the keystream

    Returns
    -------
    the ciphertext
    """
    keystream = [key] + [p for p in plaintext[:-1]]
    ciphertext = [(p + k)%26 for p, k in zip(plaintext, keystream)]
    return ciphertext

def autokey_decrypt(ciphertext: list[int], key: int) -> list[int]:
    """
    performs an autokey decryption

    Arguments
    ---------
    ciphertext: the message
    key: the first number of the keystream

    Returns
    -------
    the plaintext
    """
    plaintext = [(ciphertext[0] - key)%26]
    for i in range(1, len(ciphertext)):
        plaintext.append((ciphertext[i] - plaintext[-1])%26)
    return plaintext

def autokey_decrypt_exhaustive(ciphertext: list[int]) -> tuple[list[int], int]|None:
    """
    decrypts the autokey cipher by exhaustive search from key = 0 to 26

    Arguments
    ---------
    ciphertext: the message

    Returns
    -------
    The plaintext with the key or None for no solution found
    """
    dictionary, max_word_len = get_dictionary('./dictionary.txt')
    for key in range(26):
        message = autokey_decrypt(ciphertext, key)
        alpha_text = undigitize(message, 'plain')
        if is_valid(alpha_text, dictionary, max_word_len, 10):
            return message, key

if __name__ == '__main__':
    from ciphertext import digitize
    plaintext = 'rendezvous'
    dplaintext = digitize(plaintext)
    dciphertext = autokey_encrypt(dplaintext, 8)
    ciphertext = undigitize(dciphertext, 'cipher')
    assert ciphertext == 'ZVRQHDUJIM'
    dplaintext = autokey_decrypt(dciphertext, 8)
    plaintext = undigitize(dplaintext, 'plain')
    assert plaintext == 'rendezvous'

    ciphertext = 'MALVVMAFBHBUQPTSOXALTGVWWRG'
    dciphertext = digitize(ciphertext)
    dplaintext, key = autokey_decrypt_exhaustive(dciphertext)
    plaintext = undigitize(dplaintext, 'plain')
    print(plaintext, key)
