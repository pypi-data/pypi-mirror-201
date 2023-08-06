### Tetun Tokenizer

Tetun tokenizer is a Python package for tokenizing an input text into tokens. There are several tokenization techniques we built alongside this package as follows:
1. `TetunStandardTokenizer()`: tokenize the input text by `word`, `punctuations`, and `special characters`.
2. `TetunWhiteSpaceTokenizer()`: tokenize the input text by `whitespace` delimiter.
3. `TetunBlankLineTokenizer()`: tokenize the input text by `blank lines` delimiter.
4. `TetunSimpleTokenizer()`: tokenize the input text by extracting `only string and number` and ignore punctuations and special characters.
5. `TetunWordTokenizer()`: tokenize the input text by extracting `only string` and ignore numbers, punctuations, and special characters.

### Installation

To install Tetun tokenizer, run the following command in your console:

```
python3 -m pip install tetun-tokenizer
```

or simply run:

```
pip install tetun-tokenizer
```

It also supports `conda` and `pipenv` or similar commands.


### Usage

To use Tetun tokenizer, `from` the `tokenizer` module on the `tetuntokenizer` package, `import` a tokenizer class. Instantiate the imported class and then call a `tokenize` function as follows:

1. Using  `TetunStandardTokenizer()` to tokenize a given text.

```python
from tetuntokenizer.tokenizer import TetunStandardTokenizer

tetun_tokenizer = TetunStandardTokenizer()

text = "Ha'u mak ita-nia maluk di'ak. Ha'u iha $0.25 atu fó ba ita."
output = tetun_tokenizer.tokenize(text)
print(output)
```

The output will be:

```
["Ha'u", 'mak', 'ita-nia', 'maluk', "di'ak", '.', "Ha'u", 'iha', '$', '0.25', 'atu', 'fó', 'ba', 'ita', '.']
```

2. Using `TetunWhiteSpaceTokenizer()` to tokenize a given text.

```python
from tetuntokenizer.tokenizer import TetunWhiteSpaceTokenizer

tetun_tokenizer = TetunWhiteSpaceTokenizer()

text = "Ha'u mak ita-nia maluk di'ak. Ha'u iha $0.25 atu fó ba ita."
output = tetun_tokenizer.tokenize(text)
print(output)
```

The output will be:

```
["Ha'u", 'mak', 'ita-nia', 'maluk', "di'ak.", "Ha'u", 'iha', '$0.25', 'atu', 'fó', 'ba', 'ita.']
```

3. Using `TetunBlankLineTokenizer()` to tokenize a given text.

```python
from tetuntokenizer.tokenizer import TetunBlankLineTokenizer

tetun_tokenizer = TetunBlankLineTokenizer()

text = """
        Ha'u mak ita-nia maluk di'ak.
        Ha'u iha $0.25 atu fó ba ita.
        """
output = tetun_tokenizer.tokenize(text)
print(output)
```

The output will be:

```
["\n            Ha'u mak ita-nia maluk di'ak.\n            Ha'u iha $0.25 atu fó ba ita.\n            "]
```

4. Using `TetunSimpleTokenizer()` to tokenize a given text.

```python
from tetuntokenizer.tokenizer import TetunSimpleTokenizer

tetun_tokenizer = TetunSimpleTokenizer()

text = "Ha'u mak ita-nia maluk di'ak. Ha'u iha $0.25 atu fó ba ita."
output = tetun_tokenizer.tokenize(text)
print(output)
```

The output will be:

```
["Ha'u", 'mak', 'ita-nia', 'maluk', "di'ak", "Ha'u", 'iha', '0.25', 'atu', 'fó', 'ba', 'ita']
```

5. Using `TetunWordTokenizer()` to tokenize a given text.

```python
from tetuntokenizer.tokenizer import TetunWordTokenizer

tetun_tokenizer = TetunWordTokenizer()

text = "Ha'u mak ita-nia maluk di'ak. Ha'u iha $0.25 atu fó ba ita."
output = tetun_tokenizer.tokenize(text)
print(output)
```

The output will be:

```
["Ha'u", 'mak', 'ita-nia', 'maluk', "di'ak", "Ha'u", 'iha', 'atu', 'fó', 'ba', 'ita']
```

To print the resulting output to the console, with each element on a new line, you can use `for` loop or simply use `join()` as follows:

```
print('\n'.join(output))
```

The output will be:

```
Ha'u
mak
ita-nia
maluk
di'ak
Ha'u
iha
atu
fó
ba
ita
```

You can also use the tokenizer to tokenize a text from a file. Here is an example:

```python
# Assume that we use Path instead of a string for the file path
from pathlib import Path
from tetuntokenizer.tokenizer import TetunSimpleTokenizer


file_path = Path("myfile/example.txt")

try:
    with file_path.open('r', encoding='utf-8') as f:
    contents = [line.strip() for line in f]
except FileNotFoundError:
    print(f"File not found at: {file_path}")

# You can also lowercase the contents before tokenizing them.
lowercase_contents = contents.lower()

tetun_tokenizer = TetunSimpleTokenizer()

output = '\n'.join(tetun_tokenizer.tokenize(str(lowercase_contents)))
print(output)

```

The output will be:

```
ha'u
orgullu
dezenvolve
ha'u-nia
lian
tetun 
...
```

There are a few more ways to read file contents that you can use to achieve the same output.