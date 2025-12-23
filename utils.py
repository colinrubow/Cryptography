from numpy import unique
from math import comb


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
        dictionary = f.read().splitlines()
    # normalize to lowercase and strip empty lines
    dictionary = [w.strip().lower() for w in dictionary if w.strip()]
    # remove single-letter words except 'a' and 'i'
    dictionary = [w for w in dictionary if not (len(w) == 1 and w not in ('a', 'i'))]
    max_word_len = max((len(w) for w in dictionary)) if dictionary else 0
    return dictionary, max_word_len

def get_common_letters() -> str:
    """
    all 26 letters from most frequent to least
    """
    return 'etaoinshrdlcumwfgypbvkjxqz'

def get_common_digrams() -> list[str]:
    """
    a list of common digrams from most frequent to least
    """
    return ['th', 'he', 'in', 'er', 'an', 're', 'ed', 'on', 'es', 'st', 'en', 'at', 'to', 'nt', 'ha', 'nd', 'ou', 'ea', 'ng', 'as', 'or', 'ti', 'is', 'et', 'it', 'ar', 'te', 'se', 'hi', 'of']

def get_common_trigrams() -> list[str]:
    """
    a list of common trigrams from most frequent to least
    """
    return ['the', 'ing', 'and', 'her', 'ere', 'ent', 'tha', 'nth', 'was', 'eth', 'for', 'dth']

def get_letter_counts(text: str) -> tuple[list[str], list[int]]:
    """
    returns the letter counts of the text

    Arguments
    ---------
    text: the message

    Returns
    -------
    the first item is a list of the letters from most frequent to least. The second is the counts.
    """
    letters, counts = unique(list(text), return_counts=True)
    sorted_data = sorted(zip(letters, counts), key=lambda x: x[1], reverse=True)
    letters = [str(l) for l, _ in sorted_data]
    counts = [int(c) for _, c in sorted_data]
    return letters, counts

def get_digram_counts(text: str) -> tuple[list[str], list[int]]:
    """
    returns the digram counts of the text

    Arguments
    ---------
    text: the message

    Returns
    -------
    the first item is a list of the digrams from most frequent to least. The second is the counts.
    """
    digrams = [text[i:i+2] for i in range(len(text) - 1)]
    digrams, counts = unique(digrams, return_counts=True)
    sorted_data = sorted(zip(digrams, counts), key=lambda x: x[1], reverse=True)
    digrams = [str(l) for l, _ in sorted_data]
    counts = [int(c) for _, c in sorted_data]
    return digrams, counts

def get_trigram_counts(text: str) -> tuple[list[str], list[int]]:
    """
    returns the trigram counts of the text

    Arguments
    ---------
    text: the message

    Returns
    -------
    the first item is a list of the trigrams from the most frequent to least. The second is the counts.
    """
    trigrams = [text[i:i+3] for i in range(len(text) - 2)]
    trigrams, counts = unique(trigrams, return_counts=True)
    sorted_data = sorted(zip(trigrams, counts), key=lambda x: x[1], reverse=True)
    trigrams = [str(l) for l, _ in sorted_data]
    counts = [int(c) for _, c in sorted_data]
    return trigrams, counts

def index_of_coincidence(string: list[int]) -> float:
    """
    calculates the index of coincidence of the given string. A normal text should return about 0.065. A random string should return about 0.038

    Arguments
    ---------
    string: the message

    Returns
    -------
    the index of coincidence
    """
    n = len(string)
    freqs = [0]*27
    for character in string:
        freqs[character] += 1
    ic = sum(comb(f, 2) for f in freqs[1:])/comb(n, 2)
    return ic

def get_normal_letter_probabilities() -> list[float]:
    """
    returns a list of probabilities, A - 0 -> 0.082

    Returns
    -------
    the mapping from letter integers to their probabilities
    """
    return [0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.02, 0.061, 0.07, 0.0015, 0.008, 0.04, 0.024, 0.067, 0.075, 0.019, 0.001, 0.06, 0.063, 0.091, 0.028, 0.01, 0.023, 0.001, 0.02, 0.001]

def get_letter_freqs(text: list[int]) -> list[int]:
    """
    returns the counts for each letter in order of A to Z

    Arguments
    ---------
    text: the text in digital form

    Returns
    -------
    the counts for A, the counts for B, etc
    """
    freqs = [0]*26
    for character in text:
        freqs[character] += 1
    return freqs
