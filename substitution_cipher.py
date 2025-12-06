from ciphertext import is_valid
from utils import get_common_digrams, get_common_letters, get_common_trigrams, get_dictionary, get_digram_counts, get_letter_counts, get_trigram_counts
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
    return sub_encrypt(ciphertext, reverse_key)

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
    letters, counts = get_letter_counts(ciphertext)
    freqs = [c/len(ciphertext) for c in counts]

    key_start = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'}
    key = key_start.copy()

    cipher_freq_1 = [l for l, f in zip(letters, freqs) if f > 0.1]
    cipher_freq_2 = [l for l, f in zip(letters, freqs) if 0.05 < f <= 0.1]
    cipher_freq_3 = [l for l, f in zip(letters, freqs) if 0.03 < f <= 0.05]
    cipher_freq_4 = [l for l, f in zip(letters, freqs) if 0.0125 < f <= 0.03]
    cipher_freq_5 = [l for l, f in zip(letters, freqs) if f <= 0.0125]
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
    letter_freq = [l + f':{f:.3}' for l, f in zip(letters, freqs)]
    common_digrams = get_common_digrams()
    common_trigrams = get_common_trigrams()
    common_letters = get_common_letters()
    digrams, digram_counts = get_digram_counts(ciphertext)
    trigrams, trigram_counts = get_trigram_counts(ciphertext)

    digram_freq = [f'{str(d)}:{int(c)}' for d, c in zip(digrams, digram_counts) if c > 1]
    trigram_freq = [f'{str(t)}:{int(c)}' for t, c in zip(trigrams, trigram_counts) if c > 1]
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
