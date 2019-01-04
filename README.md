# Duolingo Word List

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cfd576be40cb40d4b86d8f6cf11a7c0a)](https://www.codacy.com/app/floscha/duolingo-word-list?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=floscha/duolingo-word-list&amp;utm_campaign=Badge_Grade)

Simple script that creates an HTML page containing all words from a Duolingo lesson, including translation and pronunciation audio.

## Usage

1. Make sure Python 3.6 is installed (older versions are not supported).
2. Install dependencies:
```
$ pip install -r dependencies.txt
```
3. Replace the placeholders in _config.yml_ with your email and authorization token.
4. Run the _main.py_:
```
$ python main.py
```
6. Open the generated _index.html_ page:
```
$ open index.html
```
