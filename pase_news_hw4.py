# 1) С помощью BeautifulSoup спарсить новости с https://news.yandex.ru по своему региону.
#
# *Заголовок
# *Краткое описание
# *Ссылка на новость

# 2) * Разбить новости по категориям
# * Расположить в хронологическом порядке

import requests
import re
import pandas as pd
from pprint import pprint
from bs4 import BeautifulSoup



def return_html_from_url(url, param_s):
    # функция по url позвращает html страницы по запросу

    headers_url = {'accept':'*/&*',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    try:
        response_request = requests.get(url,
                                        params=param_s,
                                        headers=headers_url)
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)

    return response_request.text


def find_news(html_page):

    soup = BeautifulSoup(html_page, 'html.parser')
    news_story_and_info = soup.findAll('div', {'class': re.compile('^(story story_view)')})

    news_list = []

    for new in news_story_and_info:

        new_category = new.find('a').text
        new_title = new.find('h2').find('a').text

        try:
            new_text = new.find('div', {'class': 'story__text'}).text
        except AttributeError:
            new_text = '_нет краткого описания новости_'

        new_href = 'https://news.yandex.ru' + new.find('h2').find('a')['href']
        new_time = new.find('div', {'class': 'story__date'}).text.split('\n')[1]

        dict_new = dict(zip(['category', 'title', 'text', 'url', 'time'],
                       [new_category, new_title, new_text, new_href, new_time]))

        news_list.append(dict_new)

    return pd.DataFrame(news_list, columns=dict_new.keys())


def print_result(df):

    num_news = df.shape[0]
    print(f'Найдено {num_news} новостей')
    for i in range(num_news):
        print(f'-{i + 1}-')
        print(f'"{df.iloc[i].category}"')
        print(f'=== {df.iloc[i].title} ===')
        pprint(f'{df.iloc[i].text}')
        print(f'{df.iloc[i].url}')
        print(f'{df.iloc[i].time}')
        print('==' * 30)

if __name__ == '__main__':
    param_search = {}

    html_news = return_html_from_url(f'https://news.yandex.ru/Moscow/', param_search)

    df_news = find_news(html_news).sort_values(by=['category'])

    print_result(df_news)
