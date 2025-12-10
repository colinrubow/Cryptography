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


if __name__ == '__main__':
    from ciphertext import digitize, undigitize
    plaintext = 'thiscryptosystemisnotsecure'
    key = 'cipher'
    plaintext = digitize(plaintext)
    key = digitize(key)
    ciphertext = vigenere_encrypt(plaintext, key)
    plaintext = vigenere_decrypt(ciphertext, key)
    plaintext = undigitize(plaintext, 'plain')
    print(plaintext)
