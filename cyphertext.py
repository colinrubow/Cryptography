import re


class CypherText:
    """
    Will read txt files and then be able to convert them to and from letters and digits and do cyphers on it
    """
    def __init__(self) -> None:
        self.plaintext: None|str = None
        self.dplaintext: None|list[int] = None
        self.dcyphertext: None|list[int] = None
        self.cyphertext: None|str = None
        return

    def read_file(self, file: str) -> None:
        """
        reads and stores the file into plaintext. Strips newlines

        Parameters
        ----------
        file: the directory to read from
        """
        with open(file, 'r') as f:
            text = f.read()
        text = text.lower()
        text = re.sub(r'[^a-z]+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        self.plaintext = text

    def digitize(self) -> None:
        """
        mapping 'a' -> 1, 'b' -> 2, ..., 'z' -> 26, and ' ' -> 0, digitized self.plaintext
        """
        base = ord('a') - 1
        digital = []

        if self.plaintext is None:
            raise ValueError('CypherText has not read a file yet')

        for ch in self.plaintext:
            if ch == ' ':
                digital.append(0)
            elif 'a' <= ch <= 'z':
                digital.append(ord(ch) - base)
            else:
                raise ValueError(f'Invalid character {ch} while digitizing')
        self.dplaintext = digital

    def __str__(self) -> str:
        if self.plaintext is None:
            raise ValueError('CypherText has not read a file yet')
        return f"plaintext: {self.plaintext}\n" +\
            f"dplaintext: {self.dplaintext}"

if __name__ == '__main__':
    td = CypherText()
    td.read_file('./temp.txt')
    td.digitize()
    print(td)
