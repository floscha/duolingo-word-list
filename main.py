import sys

from googletrans import Translator
import requests


def read_auth_token(file_name='auth.txt'):
    """Read authorization token from file."""
    with open(file_name, 'r') as f:
        auth_token = f.read().strip()
    return auth_token


def read_user_id(file_name='user.txt'):
    """Read user ID from file."""
    with open(file_name, 'r') as f:
        user_id = f.read().strip()
    return user_id


def print_available_lessons(language):
    """
    Print all available lessons for the given language.

    ATTENTION: Currently does not work correctly since the Duolingo API only
        allows retrieving lessons for the courses currently being learned.
    """
    authorization = read_auth_token()
    user_id = read_user_id()

    headers = {'Authorization': authorization}
    fields = 'currentCourse'
    url = f'https://www.duolingo.com/2017-06-30/users/{user_id}' + \
          f'?fields={fields}'
    r = requests.get(url, headers=headers)

    lessons = [lesson for level in r.json()['currentCourse']['skills']
               for lesson in level]
    lesson_names = [l['name'] for l in lessons]

    print("Please choose one of the following lessons:")
    for i, lesson in enumerate(lesson_names):
        print("%d. %s" % (i + 1, lesson))


def create_word_page(lesson_name, output_file='index.html'):
    translator = Translator()

    authorization = read_auth_token()

    headers = {'Authorization': authorization}
    fields = 'skills%7BlessonWords%7D'
    url = f'https://www.duolingo.com/2017-06-30/skills?fields={fields}' + \
          f'&learningLanguage={learning_language}&urlName={lesson_name}'
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

    with open(output_file, 'w') as f:
        f.write(full_page)


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) == 0:
        print("usage: main.py lang lesson")
        sys.exit(1)

    learning_language = args[0]

    if len(args) == 1:
        print_available_lessons(learning_language)
    else:
        lesson = args[1]
        create_word_page(lesson)
