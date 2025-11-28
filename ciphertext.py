import re
from typing import Callable
import numpy as np


class CipherText:
    """
    Will read txt files and then be able to convert them to and from letters and digits and do cyphers on it
    """
    def __init__(self) -> None:
        self.message: None|str|np.ndarray = None
        return

    def read(self, file: str, state: str) -> None:
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
            text = re.sub(r'[^A-Z]+', ' ', text)
            if not text.isupper():
                raise ValueError(f'given text is not all uppercase as dictated by given state: {state}')
        elif state == 'plain':
            text = re.sub(r'[^a-z]+', ' ', text)
            if not text.islower():
                raise ValueError(f'given text is not all lowercase as dictated by given state: {state}')
        else:
            raise ValueError(f'{state} is not an option. Only \'cipher\' or \'plain\'')
        text = re.sub(r'\s+', ' ', text).strip()
        self.message = text

    def digitize(self) -> None:
        """
        mapping 'a' -> 1, 'b' -> 2, ..., 'z' -> 26, and ' ' -> 0, digitized self.plaintext
        """
        if self.message is None:
            raise ValueError('message is None')

        if type(self.message) == str:
            digital = []
            if self.message.isupper():
                base = ord('A') - 1
            else:
                base = ord('a') - 1

            for ch in self.message:
                if ch == ' ':
                    digital.append(0)
                else:
                    digital.append(ord(ch) - base)
            self.message = np.array(digital)
        else:
            raise ValueError('message is already digitized')

    def undigitize(self, state: str) -> None:
        """
        turns message from a list of ints into a string

        Arguments
        ---------
        state: options are 'cipher' or 'plain', which makes the text upper or lower case respectively
        """
        if self.message is None:
            raise ValueError('message is None')

        if type(self.message) == np.ndarray:
            chars = []
            if state == 'cipher':
                base = ord('A') - 1
            elif state == 'plain':
                base = ord('a') - 1
            else:
                raise ValueError(f'state {state} is not \'cipher\' or \'plain\'')

            for val in self.message:
                if val == '0':
                    chars.append(' ')
                else:
                    chars.append(chr(base + val))
            self.message = "".join(chars)
        else:
            raise ValueError('message is already undigitized')

    def encrypt(self, method: Callable, **kwargs) -> None:
        """
        calls method with message and saves into message

        Arguments
        ---------
        method: the method used to encrypt such as shift cipher. First argument should be the digitezed plaintext
        kwargs: arguments used for method
        """
        if self.message is None:
            raise ValueError('CipherText has not read a plaintext file yet')

        self.message = method(self.dplaintext, kwargs)

    def decrypt(self, method: Callable, **kwargs) -> None:
        """
        calls method with message and saves into message

        Arguments
        ---------
        method: the method used to decrypt such as exhaustive search for a shift cipher. First argument should be message, the second is the validity test
        kwargs: arguments used for method
        """
        if self.message is None:
            raise ValueError('CipherText has not read a ciphertext file yet')

        self.dplaintext = method(self.message, self.is_valid, kwargs)

    def is_valid(self) -> bool:
        """
        checks if the message is valid by seeing if successive words are in a dictionary
        """
        if self.message is None:
            raise ValueError('CipherText has not read a file yet')
        if type(self.message) == list:
            raise ValueError('message is not a string')

        with open('./dictionary.txt', 'r') as f:
            dictionary = f.read()
        dictionary = dictionary.split('\n')
        test = [1 if word in dictionary else 0 for word in self.message[:20]]
        if sum(test) >= 15:
            return True
        return False

    def __str__(self) -> str:
        if self.message is not None:
            if type(self.message) == str:
                return self.message
            else:
                return self.message.__str__()
        else:
            return super().__str__()
