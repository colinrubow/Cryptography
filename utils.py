import numpy as np

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
    letters, counts = np.unique(list(text), return_counts=True)
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
    digrams, counts = np.unique(digrams, return_counts=True)
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
    trigrams, counts = np.unique(trigrams, return_counts=True)
    sorted_data = sorted(zip(trigrams, counts), key=lambda x: x[1], reverse=True)
    trigrams = [str(l) for l, _ in sorted_data]
    counts = [int(c) for _, c in sorted_data]
    return trigrams, counts
