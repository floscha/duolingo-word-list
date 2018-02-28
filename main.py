from googletrans import Translator
import requests


if __name__ == '__main__':
    translator = Translator()

    # Read authorization token from file.
    with open('auth.txt', 'r') as f:
        authorization = f.read().strip()

    headers = {'Authorization': authorization}
    fields = 'skills%7BlessonWords%7D'
    learning_language = 'zh'
    url_name = 'Numbers-1'
    url = f'https://www.duolingo.com/2017-06-30/skills?fields={fields}' + \
          f'&learningLanguage={learning_language}&urlName={url_name}'
    r = requests.get(url, headers=headers)

    nested_word_list = r.json()['skills'][0]['lessonWords']
    flattened_word_list = [word for sublist in nested_word_list
                           for word in sublist]
    print(flattened_word_list)

    translations = [translator.translate(word).text.lower() for word in flattened_word_list]
    print(translations)

    script_section = '<script src="https://code.responsivevoice.org/responsivevoice.js"></script>'
    page_template = (f'<header>{script_section}</header>' +
                     '<body>%s</body>')
    word_links = [f'<a onclick="responsiveVoice.speak(\'{word}\', \'Chinese Female\');" href="">{word}</a> - <a onclick="responsiveVoice.speak(\'{trans}\', \'UK English Female\');" href="">{trans}</a><br/>'
                  for word, trans in zip(flattened_word_list, translations)]
    joined_word_links = ' '.join(word_links)

    full_page = page_template % joined_word_links

    with open('index.html', 'w') as f:
        f.write(full_page)
