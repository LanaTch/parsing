# 2. В приложении парсинга википедии получить первую ссылку на другую страницу
# и вывести все значимые слова из неё. Результат записать в файл в форматированном виде

import collections
import requests
import re


def return_html_from_url(topic_url):
    wiki_request = requests.get(topic_url)
    # print(wiki_request.content)
    return wiki_request.text


def find_first_url(wiki_text):
    pattern = r'title=\"Редактировать раздел «Ссылки»\"(.{1,})\n(<ul>(.{1,}))'
    spam = re.findall(pattern, wiki_text)

    pattern_link = r'href=\"(.*?)\"'
    links = re.findall(pattern_link, str(spam))

    first_link = links[1]
    # print(first_link)

    return first_link


def return_words(topic_url):
    text_html = return_html_from_url(topic_url)
    #print(text_html)
    words = re.findall('[a-zA-Z]{3,}', text_html)
    words_counter = collections.Counter()
    for word in words:
        words_counter[word] += 1

    return words_counter.most_common(10)

def write_output_file(words_most_common):
    f = open('words_most_common.txt', 'w', encoding='utf-8')
    for word in words_most_common:
        f.write(f'Слово {word[0]} встречается {word[1]} раз\n')
    f.close()

# ссылка на топик википедии
wiki_url = f'https://ru.wikipedia.org/wiki/' \
    f'%D0%9C%D0%B0%D1%88%D0%B8%D0%BD%D0%BD%D0%BE%D0%B5_' \
    f'%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5'

# получаем html-текст из get-запроса по ссылке
wiki_text = return_html_from_url(wiki_url)

# ищем первую ссылку из раздела Ссылки
first_url = find_first_url(wiki_text)

# считаем слова, которые есть на странице по найденной ссылке
words = return_words(first_url)

# запись результатов в файл
write_output_file(words)
