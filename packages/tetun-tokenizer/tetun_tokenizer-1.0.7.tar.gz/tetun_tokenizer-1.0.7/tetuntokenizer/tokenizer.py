""" 
A contribution from Gabriel de Jesus (https://www.linkedin.com/in/gabrieljesus/)
as part of his Ph.D. research work. 

The Tetun tokenizer supports the following tokenization techniques:
* tokenize the input string by word, punctuations, or special characters delimiters.
* tokenize the input string by whitespace delimiter.
* tokenize the input string by blank lines delimiter.
* tokenize the input string by extracting only string and number and ignore punctuations and special characters.
* tokenize the input string by extracting only string and ignore numbers, punctuations, and special characters.

Note: please cite tetun-tokenizer if you use it for scientific publication purposes or contribute to a community.
"""
import re
from typing import List

PUNCTUATIONS = '.,:;?!-"“”/\\<>()[]{}'
SPECIAL_CHARS = '#$€%@*&_|=+^`~<<>>'


class TetunRegexTokenizer:
    """Tokenizes a string (or text) using regular expressions."""

    def __init__(self, patterns: str, split: bool = False) -> None:
        """
        :param patterns: a regular expression to match the tokens.
        :param split: if True, use re.split() to tokenize text, else use re.findall().            
        """
        self.patterns = patterns
        self.split = split

    def tokenize(self, text: str) -> List[str]:
        """ 
        :param text: the text to be tokenized.
        :return: a list of tokens.
        """
        if self.split:
            tokens = re.split(self.patterns, text)
        else:
            tokens = re.findall(self.patterns, text)
        return tokens


class TetunStandardTokenizer(TetunRegexTokenizer):
    """ Tokenize a string (or text) by word, punctuations, and special characters delimiters. """

    def __init__(self) -> None:
        patterns = (
            # e.g.: Área, área, ne'e, Ne'ebé, kompañia, ida-ne'e, ida-ne'ebé, etc.
            # e.g. person names: Ângelo, Adão, Érica, etc.
            r"[A-Za-zÂÁáãéêÉÊíÍóÓúÚñç]+(?:[-’'][A-Za-zÂÁáãéêÉÊíÍóÓúÚñç]+)*"
            r"|"
            r"[\d]+[\.\d]*[\,\d]*"
            r"|"
            r"[" + re.escape("".join(PUNCTUATIONS + SPECIAL_CHARS)) + "]"
        )
        super().__init__(patterns)


class TetunWhiteSpaceTokenizer(TetunRegexTokenizer):
    """ Tokenize text by whitespace delimiter. """

    def __init__(self) -> None:
        patterns = r"\s+"
        super().__init__(patterns, split=True)


class TetunBlankLineTokenizer(TetunRegexTokenizer):
    """ Tokenize a string (or text), treating any sequence of blank lines as a delimiter. """

    def __init__(self) -> None:
        patterns = r"s*\n\s*\n\s*"
        super().__init__(patterns, split=True)


class TetunSimpleTokenizer(TetunRegexTokenizer):
    """ Tokenize a string (or text) and numbers and ignore punctuations and special characters. """

    def __init__(self) -> None:
        patterns = (
            r"[A-Za-zÂÁáãéêÉÊíÍóÓúÚñç]+(?:[-’'][A-Za-zÂÁáãéêÉÊíÍóÓúÚñç]+)*"
            r"|"
            r"[\d]+[\.\d]*[\,\d]*"
        )
        super().__init__(patterns)


class TetunWordTokenizer(TetunRegexTokenizer):
    """ Tokenize a string (or text) and ignore numbers, punctuations and special characters. """

    def __init__(self) -> None:
        patterns = (
            r"[A-Za-zÂÁáãéêÉÊíÍóÓúÚñç]+(?:[-’'][A-Za-zÂÁáãéêÉÊíÍóÓúÚñç]+)*"
        )
        super().__init__(patterns)
