from math import gcd


def vigenere_encrypt(plaintext: list[int], key: list[int]) -> list[int]:
    """
    performs a vigenere encryption by c = p + key

    Arguments
    ---------
    plaintext: the message
    key: the shift word

    Returns
    -------
    the ciphertext
    """
    ciphertext = plaintext.copy()

    for i in range(len(ciphertext)):
        ciphertext[i] = (ciphertext[i] + key[i%len(key)])%26

    return ciphertext

def vigenere_decrypt(ciphertext: list[int], key: list[int]) -> list[int]:
    """
    performs a vigenere decryption by c = p - key

    Arguments
    ---------
    ciphertext: the message
    key: this shift word

    Returns
    -------
    the plaintext
    """
    plaintext = ciphertext.copy()

    for i in range(len(plaintext)):
        plaintext[i] = (plaintext[i] - key[i%len(key)])%26

    return plaintext

def kasiski_test(ciphertext: list[int], length: int = 3) -> int:
    """
    attempts to determine the length of the keyword using the kasiski test: a vigenere cipher will encode the same plaintext the same way at equal increments

    Arguments
    ---------
    ciphertext: the text
    length: the length of the string to check for repeated values
    """
    # get all substrings of length length
    substrings = [ciphertext[i:i+length] for i in range(len(ciphertext) - length + 1)]

    # get most frequent substring
    substring_most = max(substrings, key = substrings.count)

    # get the indices of the substrings
    indices = [i for i in range(len(substrings)) if substrings[i] == substring_most]

    # get the diffs
    diffs = [i - indices[0] for i in indices]

    # get the gcd
    return gcd(*diffs[1:])
