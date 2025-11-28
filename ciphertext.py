import re
from typing import Literal
import numpy as np


def read(file: str, state: str) -> str:
    """
    reads a txt file. Strips newlines

    Arguments
    ---------
    file: the directory
    state: options are 'cipher' or 'plain'
    """
    with open(file, 'r') as f:
        text = f.read()
    if state == 'cipher':
        text = re.sub(r'[^A-Z]+', '', text)
        if not text.isupper():
            raise ValueError(f'given text is not all uppercase as dictated by given state: {state}')
    elif state == 'plain':
        text = re.sub(r'[^a-z]+', '', text)
        if not text.islower():
            raise ValueError(f'given text is not all lowercase as dictated by given state: {state}')
    else:
        raise ValueError(f'{state} is not an option. Only \'cipher\' or \'plain\'')
    text = re.sub(r'\s+', '', text).strip()
    return text

def digitize(message: str) -> np.ndarray:
    """
    mapping 'a' -> 1, 'b' -> 2, ..., 'z' -> 26, and ' ' -> 0, digitized self.plaintext

    Arguments
    ---------
    text: the alpha text

    Returns
    -------
    the list of digital numbers
    """
    digital = []
    if message.isupper():
        base = ord('A')
    else:
        base = ord('a')

    for ch in message:
        digital.append(ord(ch) - base)
    return np.array(digital)

def undigitize(message: np.ndarray, state: Literal['cipher', 'plain']) -> str:
    """
    turns message from a list of ints into a string

    Arguments
    ---------
    message: the digital array
    state: options are 'cipher' or 'plain', which makes the text upper or lower case respectively

    Returns
    -------
    the string alpha message
    """
    chars = []
    if state == 'cipher':
        base = ord('A')
    elif state == 'plain':
        base = ord('a')

    for val in message:
        chars.append(chr(base + val))
    return "".join(chars)

def get_dictionary(file: str) -> tuple[list[str], int]:
    """
    reads a dictionary and splits it into a list

    Arguments
    ---------
    file: the directory of the dictionary

    Returns
    -------
    the dictionary and the max word length
    """
    with open(file, 'r') as f:
        dictionary = f.read()
    dictionary = dictionary.split('\n')
    for letter in ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
        dictionary.remove(letter)
    max_word_len = max((len(w) for w in dictionary))
    return dictionary, max_word_len

def is_valid(message: str, dictionary: list[str], max_word_len: int) -> bool:
    """
    checks if the message is valid by seeing if successive words are in a dictionary

    Arguments
    ---------
    message: the alpha message
    dictionary: the dictionary, duh
    max_word_len: the longest word length in the dictionary

    Returns
    -------
    as expected
    """
    n = len(message)
    max_word_len = min(max_word_len, n)
    dp = [False]*(n + 1)
    prev = [-1]*(n+1)
    dp[0] = True

    for i in range(1, n + 1):
        start = max(0, i - max_word_len)
        for j in range(start, i):
            if dp[j]:
                word = message[j:i]
                if word in dictionary:
                    dp[i] = True
                    prev[i] = j
                    break

    if not dp[n]:
        return False
    return True
