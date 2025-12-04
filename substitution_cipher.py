import numpy as np
from ciphertext import digitize, undigitize, is_valid, get_dictionary
import ciphertext
import os


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
    performs decryption using character frequency, (e is most common), and digrams and such with user interaction

    Arguments
    ---------
    ciphertext: the message to decrypt

    Returns
    -------
    the plaintext with the key or None if no solution is found
    """
    dictionary, max_word_len = get_dictionary('./dictionary.txt')

    # freq of 0.12
    letter_freq_1 = 'e'
    # freq from 0.06 to 0.09
    letter_freq_2 = 'taoinshr'
    # freq of 0.04
    letter_freq_3 = 'dl'
    # freq from 0.015 to 0.028
    letter_freq_4 = 'cumwfgypb'
    # freq less than 0.01
    letter_freq_5 = 'vkjxqz'
    letter_freqs = [letter_freq_1, letter_freq_2, letter_freq_3, letter_freq_4, letter_freq_5]

    # get freq of letters in ciphertext
    letters, counts = np.unique(list(ciphertext), return_counts=True)
    freqs = [c/len(ciphertext) for c in counts]

    # sort from most frequent to least
    sorted_data = sorted(zip(letters, freqs), key=lambda x: x[1], reverse=True)
    letters = [l for l, _ in sorted_data]
    freqs = [f for _, f in sorted_data]

    key_start = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'}
    key = key_start.copy()

    cipher_freq_1 = [l for l, f in sorted_data if f > 0.1]
    cipher_freq_2 = [l for l, f in sorted_data if 0.05 < f <= 0.1]
    cipher_freq_3 = [l for l, f in sorted_data if 0.03 < f <= 0.05]
    cipher_freq_4 = [l for l, f in sorted_data if 0.0125 < f <= 0.03]
    cipher_freq_5 = [l for l, f in sorted_data if f <= 0.0125]
    cipher_freqs = [cipher_freq_1, cipher_freq_2, cipher_freq_3, cipher_freq_4, cipher_freq_5]

    # most likey guess to get started
    for i in range(len(cipher_freqs)):
        cipher_freq = cipher_freqs[i]
        letter_freq = letter_freqs[i]
        if len(cipher_freq) > len(letter_freq):
            cipher_freqs[i+1] = cipher_freq[len(letter_freq):] + cipher_freqs[i+1]
            cipher_freq = cipher_freq[:len(letter_freq)]
        for j in range(len(cipher_freq)):
            key[cipher_freq[j]] = letter_freq[j]
    plaintext = ''.join([key[c] for c in ciphertext])
    if is_valid(plaintext, dictionary, max_word_len):
        return plaintext, key
    else:
        plaintext = ''.join(['-']*len(ciphertext))

    # start interacting
    letter_freq = [l + f':{f:.3}' for l, f in sorted_data]
    common_digrams = ['th', 'he', 'in', 'er', 'an', 're', 'ed', 'on', 'es', 'st', 'en', 'at', 'to', 'nt', 'ha', 'nd', 'ou', 'ea', 'ng', 'as', 'or', 'ti', 'is', 'et', 'it', 'ar', 'te', 'se', 'hi', 'of']
    common_trigrams = ['the', 'ing', 'and', 'her', 'ere', 'ent', 'tha', 'nth', 'was', 'eth', 'for', 'dth']
    common_letters = 'etaoinshrdlcumwfgypbvkjxqz'
    digrams = [ciphertext[i:i+2] for i in range(len(ciphertext)-1)]
    trigrams = [ciphertext[i:i+3] for i in range(len(ciphertext)-2)]
    digram_freq, counts = np.unique(digrams, return_counts=True)
    digram_freq = [f'{str(d)}:{int(c)}' for d, c in zip(digram_freq, counts) if c > 1]
    digram_freq.sort(key=lambda x: int(x[3]), reverse=True)
    trigram_freq, counts = np.unique(trigrams, return_counts=True)
    trigram_freq = [f'{str(t)}:{int(c)}' for t, c in zip(trigram_freq, counts) if c > 1]
    trigram_freq.sort(key=lambda x: int(x[4]), reverse=True)
    key = key_start.copy()
    while True:
        os.system('cls')
        print('Current Plaintext/Ciphertext Guess:\n')
        length = 160
        for i in range(int(len(ciphertext)/length)+1):
            j = i*length
            print(plaintext[j:j+length])
            print(ciphertext[j:j+length])
            print()
        print('With the Current Key:\n')
        print({k:v for k, v in key.items() if v.islower()})
        print()
        print('Letter Freq:\n')
        print(letter_freq)
        print()
        print('Common Letters:\n')
        print(common_letters)
        print()
        print('Digram Freq:\n')
        print(digram_freq)
        print()
        print('Common Digrams:\n')
        print(common_digrams)
        print()
        print('Trigram Freq:\n')
        print(trigram_freq)
        print()
        print('Common Trigrams:\n')
        print(common_trigrams)
        print()
        command = input('Options: (Y) if valid, (N) if giving up, (R) reset, (Ab) for substitution: ')
        if command == 'Y':
            return plaintext, key
        elif command == 'N':
            return None
        elif command == 'R':
            key = key_start.copy()
            plaintext = ''.join(['-']*len(ciphertext))
        elif len(command) != 2 or command[0].islower():
            continue
        else:
            key[command[0]] = command[1]
            plaintext = ''.join([key[c] if key[c].islower() else '-' for c in ciphertext])
            if '-' not in plaintext:
                if is_valid(plaintext, dictionary, max_word_len):
                    return plaintext, key
