import numpy as np
from ciphertext import digitize, undigitize, is_valid, get_dictionary
import ciphertext


def sub_encrypt(plaintext: str, key: dict) -> str:
    """
    performs a substitution cipher encryption by the obvious

    Arguments
    ---------
    plaintext: the message
    key: the substitution key

    Returns
    -------
    the ciphertext
    """
    ciphertext = [key[t] for t in plaintext]
    return ''.join(ciphertext)

def sub_decrypt(ciphertext: str, key: dict) -> str:
    """
    performs substitution decryption by the reverse of the key

    Arguments
    ---------
    ciphertext: the encrypted message
    key: the substitution key

    Returns
    -------
    the plaintext
    """
    reverse_key = {v: k for k, v in key.items()}
    plaintext = [reverse_key[c] for c in ciphertext]
    return ''.join(plaintext)

def sub_decrypt_frequency(ciphertext: str) -> tuple[str, dict]|None:
    """
    performs decryption using character frequency, (e is most common), and digrams and such

    Arguments
    ---------
    ciphertext: the message to decrypt

    Returns
    -------
    the plaintext with the key or None if no solution is found
    """
    dictionary, max_word_len = get_dictionary('./dictionary.txt')

    # freq of 0.12
    letter_freq_1 = 'E'
    # freq from 0.06 to 0.09
    letter_freq_2 = 'TAOINSHR'
    # freq of 0.04
    letter_freq_3 = 'DL'
    # freq from 0.015 5o 0.028
    letter_freq_4 = 'CUMWFGYPB'
    # freq less than 0.01
    letter_freq_5 = 'VKJXQZ'

    # NOTE: perhaps include common digram and trigram?

    # get freq of letters in ciphertext
    letters, counts = np.unique(list(ciphertext), return_counts=True)
    freqs = [c/len(ciphertext) for c in counts]

    # sort from most frequent to least
    sorted_data = sorted(zip(letters, freqs), key=lambda x: x[1], reverse=True)
    letters = [l for l, _ in sorted_data]
    freqs = [f for _, f in sorted_data]

    key = {'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd', 'E': 'e', 'F': 'f', 'G': 'g', 'H': 'h', 'I': 'i', 'J': 'j', 'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n', 'O': 'o', 'P': 'p', 'Q': 'q', 'R': 'r', 'S': 's', 'T': 't', 'U': 'u', 'V': 'v', 'W': 'w', 'X': 'x', 'Y': 'y', 'Z': 'z'}

    cipher_freq_1 = [l for l, f in sorted_data if f > 0.1]
    cipher_freq_2 = [l for l, f in sorted_data if 0.05 < f <= 0.1]
    cipher_freq_3 = [l for l, f in sorted_data if 0.03 < f <= 0.05]
    cipher_freq_4 = [l for l, f in sorted_data if 0.0125 < f <= 0.03]
    cipher_freq_5 = [l for l, f in sorted_data if f <= 0.0125]



if __name__ == '__main__':
    message = 'EMGLOSUDCGDNCUSWYSFHNSFCYKDPUMLWGYICOXYSIPJCKQPKUGKMGOLICGINCGACKSNISACYKZSCKZECJCKSHYSXCGOIDPKZCNKSHICGIWYGKKGKGOLDSILKGOIUSIGLEDSPWZUGFZCCNDGYYSFUSZCNXEOJNCGYEOWEUPXEZGACGNFGLKNSACIGOIYCKXCJUCIUZCFZCCNDGYYSFEUEKUZCSOCFZCCNCIACZEJNCSHFZEJZEGMXCYHCJUMGKUCY'

    sub_decrypt_frequency(message)
