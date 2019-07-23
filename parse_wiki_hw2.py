# 2. В приложении парсинга википедии получить первую ссылку на другую страницу
# и вывести все значимые слова из неё. Результат записать в файл в форматированном виде

import collections
import requests
import re
import lxml.html
import pprint


def return_wiki_html(topic):
    wiki_request = requests.get(f'https://ru.wikipedia.org/wiki/{topic.capitalize()}')
    # print(wiki_request.content)
    return wiki_request.text


def find_first_url(wiki_text):
    first_url = re.findall('(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)'
                           '(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#/%=~_|$?!:,.])*'
                           '(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[A-Z0-9+&@#/%=~_|$])',
                           wiki_text)
    return first_url


def return_words(topic):
    wiki_html = return_wiki_html(topic)
    words = re.findall('[а-яА-Я]{3,}', wiki_html)
    words_counter = collections.Counter()
    for word in words:
        words_counter[word] += 1
    for word in words_counter.most_common(10):
        print(f'Слово {word[0]} встречается {word[1]} раз')
    return words_counter.most_common(10)


# 'https://en.wikipedia.org/wiki/City_Newspaper'
wiki_text = return_wiki_html('Трям!_Здравствуйте!')

doc = lxml.html.document_fromstring(wiki_text)
links = doc.xpath('//*[@id="mw-pages"]//li[a]/a')
for link in links:
  print(link.get('href'))
# pprint.pprint(wiki_req.json())
# pprint.pprint(wiki_text)
# f = open('wiki.txt', 'w', encoding='utf-8')
# pprint.pprint(find_first_url(wiki_text))
# f.write(wiki_text)
# f.close()
