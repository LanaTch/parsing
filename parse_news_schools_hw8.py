# Парсер находит 5 последних новостей с двух школ и музыкальной школы
# и печатает их на экран. Программа простая, но лично мне полезная,
# потренировалась в bs4

import requests
from bs4 import BeautifulSoup


def request_to_site(url, params=None):

    headers_my = {'accept': '*/&*',
                  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    try:
        request = requests.get(url, params=params, headers=headers_my)

        return BeautifulSoup(request.text, 'html.parser')
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


def parse_sch(number_sch):

    soup = request_to_site(f'https://sch{number_sch}zg.mskobr.ru/novosti')
    news_info = soup.findAll('div', {'class': 'kris-news-box'}, limit=5)

    print('='*30)
    print(f'----новости школы {number_sch}----')
    print('='*30)
    for new in news_info:
        link = f"https://sch{number_sch}zg.mskobr.ru{new.find('a')['href']}"
        print(link)
        print(''.join(new.find('div', {'class': 'kris-news-data-txt'}).text.split()))
        print(' '.join(new.find('a').text.split()))
        print(' '.join(new.find('div', {'class': 'kris-news-body'}).text.split()))
        print('='*40)


def parse_music_sch():

    soup = request_to_site('https://musorgskiy.music.mos.ru/press/news/')
    news_info = soup.findAll('dd', limit=5)

    print('='*30)
    print(f'---- новости музыкальной школы ----')
    print('='*30)
    for new in news_info:
        link = f"https://musorgskiy.music.mos.ru{new.find('a')['href']}"
        print(link)
        print(' '.join(new.find('a').text.split()))
        print(' '.join(new.find('div', {'class': 'b-newspreview'}).text.split()))
        print('='*40)


parse_sch('853')
print()
print()
parse_sch('2045')
print()
print()
parse_music_sch()
