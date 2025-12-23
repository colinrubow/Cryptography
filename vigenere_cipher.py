from math import gcd
from utils import get_letter_freqs, get_normal_letter_probabilities, index_of_coincidence
from numpy import mean


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

def kasiski_test(ciphertext: list[int], length: int = 3) -> tuple[int, int]:
    """
    attempts to determine the length of the keyword using the kasiski test: a vigenere cipher will encode the same plaintext the same way at equal increments

    Arguments
    ---------
    ciphertext: the text
    length: the length of the string to check for repeated values

    Returns
    -------
    the likely key length, the number of substrings of length length
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
    return gcd(*diffs[1:]), len(indices)

def divide_string_by_index(text: list[int], num_subsets: int) -> list[list[int]]:
    """
    puts the text into boxes according to their index. If num_subsets is 3, then text[i] -> box[i%num_subsets]

    Arguments
    ---------
    text: the text
    num_subsets: the number of boxes to seperate text into

    Returns
    -------
    the boxes
    """
    boxes = [[] for _ in range(num_subsets)]
    for i, character in enumerate(text):
        boxes[i%num_subsets].append(character)
    return boxes

def index_of_coincidence_test(ciphertext: list[int], length: int = 3) -> float:
    """
    computes the median index of coincidence after splitting ciphertext according to length

    Arguments
    ---------
    ciphertext: the message
    length: the len of the keyword

    Returns
    -------
    the median index of coincidence
    """
    substrings = divide_string_by_index(ciphertext, length)
    ics = [index_of_coincidence(substring) for substring in substrings]
    return float(mean(ics))

def get_key_length_kasiski(ciphertext: list[int], limit: int) -> int:
    """
    attempts to determine the length of the keyword with the kasiski test. Will decide a key length by the non-zero kasiski_test value with the most substring occurances.

    Arguments
    ---------
    ciphertext: the text
    limit: the highest number to test

    Returns
    -------
    the length of the key
    """
    best_length, best_num_subs = 1, 1

    for i in range(3, limit + 1):
        m, n_subs = kasiski_test(ciphertext, i)
        if n_subs > best_num_subs:
            best_length = m
            best_num_subs = n_subs
    return best_length

def get_key_length_index_coincidence(ciphertext: list[int], limit: int) -> int:
    """
    attempts to determine the length of the keyword with the index of coincidence. Will decide a key length by the index_of_coincidence closest to 0.065 up to the limit

    Arguments
    ---------
    ciphertext: the message
    limit: the highest number to test

    Returns
    -------
    the length of the key
    """
    best_length, best_distance = 0, 2

    for i in range(3, limit + 1):
        ic = index_of_coincidence_test(ciphertext, i)
        distance = abs(ic - 0.065)
        if distance < best_distance:
            best_distance = distance
            best_length = i
    return best_length

def vigenere_decrypt_kasiski_index(ciphertext: list[int], method: str) -> tuple[list[int], list[int]]:
    """
    attempts to decrypt using the kasiski test and/or index of coincidence to get the length of the keyword, then using the index of coincidence to find the keyword

    Arguments
    ---------
    ciphertext: the message
    method: one of 'kasiski', 'index', or 'both'

    Returns
    -------
    the plaintext
    """
    match method:
        case 'kasiski':
            m = get_key_length_kasiski(ciphertext, 10)
        case 'index':
            m = get_key_length_index_coincidence(ciphertext, 10)
        case 'both':
            m_kasiski = get_key_length_kasiski(ciphertext, 10)
            m_index = get_key_length_index_coincidence(ciphertext, 10)
            if m_kasiski != m_index:
                raise ValueError(f'm_kasiski: {m_kasiski}, m_index: {m_index} don\'t agree')
            m = m_kasiski
        # default case
        case _:
            raise ValueError(f'method {method} is not valid. Should be kasiski, index, or both')

    key = []
    p = get_normal_letter_probabilities()
    substrings = divide_string_by_index(ciphertext, m)
    for i in range(m):
        key_best = 0
        mg_best = 0
        freqs = get_letter_freqs(substrings[i])
        for j in range(1, 27):
            mg = sum([p[k]*freqs[(k+j)%26] for k in range(26)])/len(substrings[i])
            if mg > mg_best:
                mg_best = mg
                key_best = j
        key.append(key_best)
    plaintext = vigenere_decrypt(ciphertext, key)
    return plaintext, key
