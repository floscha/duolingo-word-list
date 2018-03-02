import sys

from googletrans import Translator
import requests


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) < 2:
        print("usage: main.py lang lesson")
        sys.exit(1)

    learning_language = args[0]
    lesson = args[1]

    translator = Translator()

    # Read authorization token from file.
    with open('auth.txt', 'r') as f:
        authorization = f.read().strip()

    headers = {'Authorization': authorization}
    fields = 'skills%7BlessonWords%7D'
    url = f'https://www.duolingo.com/2017-06-30/skills?fields={fields}' + \
          f'&learningLanguage={learning_language}&urlName={lesson}'
    r = requests.get(url, headers=headers)

    nested_word_list = r.json()['skills'][0]['lessonWords']
    flattened_word_list = [word for sublist in nested_word_list
                           for word in sublist]
    print(flattened_word_list)

    translations = [translator.translate(word).text.lower()
                    for word in flattened_word_list]
    print(translations)

    # Load templates.
    with open('templates/page.html', 'r') as f:
        page_template = f.read()
    with open('templates/word.html', 'r') as f:
        word_template = f.read()

    word_links = [word_template.format_map({'word': word,
                                            'translation': trans})
                  for word, trans in zip(flattened_word_list, translations)]
    joined_word_links = ' '.join(word_links)

    full_page = page_template.format(joined_word_links)

    with open('index.html', 'w') as f:
        f.write(full_page)
