import sys

from googletrans import Translator
import requests
import yaml


def read_config(file_name='config.yml'):
    """Read configuration from YAML file.

    Configuration currently contains:
        - User ID ('user_id')
        - Authorization token ('auth')
    """
    with open(file_name, 'r') as f:
        configuration = yaml.load(f)
    return configuration


def print_available_lessons(language):
    """
    Print all available lessons for the given language.

    ATTENTION: Currently does not work correctly since the Duolingo API only
        allows retrieving lessons for the courses currently being learned.
    """
    authorization = config['auth']
    user_id = config['user_id']

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


def get_lessons_words(lesson_name):
    authorization = config['auth']

    headers = {'Authorization': authorization}
    fields = 'skills%7BlessonWords%7D'
    url = f'https://www.duolingo.com/2017-06-30/skills?fields={fields}' + \
          f'&learningLanguage={learning_language}&urlName={lesson_name}'
    r = requests.get(url, headers=headers)

    nested_word_list = r.json()['skills'][0]['lessonWords']
    flattened_word_list = [word for sublist in nested_word_list
                           for word in sublist]

    print(flattened_word_list)
    return flattened_word_list


def create_word_page(words, output_file='index.html'):
    translator = Translator()

    translations = [translator.translate(word).text.lower()
                    for word in words]
    print(translations)

    # Load templates.
    with open('templates/page.html', 'r') as f:
        page_template = f.read()
    with open('templates/word.html', 'r') as f:
        word_template = f.read()

    word_links = [word_template.format_map({'word': word,
                                            'translation': trans})
                  for word, trans in zip(words, translations)]
    joined_word_links = ' '.join(word_links)

    full_page = page_template.format_map(
        {'learning_language': learning_language,
         'content': joined_word_links})

    with open(output_file, 'w') as f:
        f.write(full_page)


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) == 0:
        print("usage: main.py lang lesson")
        sys.exit(1)

    config = read_config()

    learning_language = args[0]

    if len(args) == 1:
        print_available_lessons(learning_language)
    else:
        lesson = args[1]
        words = get_lessons_words(lesson)
        create_word_page(words)
