from utils import get_dictionary
from ciphertext import is_valid


def permute_encrypt(plaintext: list[str], key: list[int]) -> list[str]:
    """
    encryptes the text by permuting every m=len(key) characters according to the key. The key indexes from 0.

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
        ciphertext = plaintext + ['a']*(m - edge)
    else:
        ciphertext = plaintext.copy()

    for i in range(0, len(ciphertext), m):
        ciphertext[i:i+m] = [ciphertext[i:i+m][k] for k in key]
    return ciphertext

def permute_decrypt(ciphertext: list[str], key: list[int]) -> list[str]:
    """
    decrypts the text by permuting every m=len(key) characters according to the inverse permuation of the key. The key indexes from 0.

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

def permute_mod_class_encrypt(plaintext: list[str], key: int) -> list[str]:
    """
    encrypts a permutation by sorting the letters into classes mod key

    Arguments
    ---------
    plaintext: the message
    key: the number of classes

    Returns
    -------
    the ciphertext
    """
    block = [[plaintext[i] for i in range(len(plaintext)) if i%key == n] for n in range(key)]
    ciphertext = []
    for text in block:
        ciphertext.extend(text)
    return ciphertext

def permute_mod_class_decrypt(ciphertext: list[str], key: int) -> list[str]:
    """
    decrypts a permutation by unsorting the letteres from their classes mod key

    Arguments
    ---------
    ciphertext: the message
    key: the number of classes

    Returns
    -------
    the plaintext
    """
    key = len(ciphertext)//key
    return permute_mod_class_encrypt(ciphertext, key)

def permute_mod_class_decrypt_exhaustive(ciphertext: list[str]) -> tuple[list[str], int]:
    """
    decrypts a mod class permutation encryption by checking each mod class

    Arguments
    ---------
    ciphertext: the message

    Returns
    -------
    the plaintext and the key
    """
    dictionary, max_word_len = get_dictionary('./dictionary.txt')

    for key in range(2, len(ciphertext)):
        plaintext = permute_mod_class_decrypt(ciphertext, key)
        # combine all chars in plaintext into a single str
        plaintext = "".join(plaintext)
        if is_valid(plaintext, dictionary, max_word_len, 20):
            return list(plaintext), key
    return [""], 0
