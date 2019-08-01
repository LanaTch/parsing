# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные объявления с avito.ru в созданную БД (xpath/BS для парсинга на выбор)

# 2) Написать функцию, которая производит поиск и выводит на экран объявления с ценой меньше
# введенной суммы

# *Написать функцию, которая будет добавлять в вашу базу данных только новые объявления


from pprint import pprint
import re
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests


client = MongoClient('mongodb://127.0.0.1:27017')
db = client['ads']
ads_db = db.ads


def request_to_site():

    try:
        request = requests.get('https://www.avito.ru/moskva_i_mo/bytovaya_tehnika')
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)
    return request.text



def save_to_mongo_db():
    ads_db.drop()

    html_page = request_to_site()
    soup = BeautifulSoup(html_page, 'html.parser')

    ads = soup.find_all('div', class_=re.compile('^(description)'))

    for ad in ads:
        price_spam = ad.find('span', class_=re.compile('^(price)')).text
        try:
            price = int(''.join(filter(lambda x: x.isdigit(), price_spam)))
        except ValueError:
            price = 0
        a_info_ad = ad.find('a')
        data_ad = dict(zip(['title', 'link', 'price'],
                           [a_info_ad['title'], f'https://www.avito.ru/{a_info_ad["href"]}', price]))
        ads_db.insert_one(data_ad)
        print('Record added')



def save_only_new_to_mongo_db():
    html_page = request_to_site()
    soup = BeautifulSoup(html_page, 'html.parser')

    ads = soup.find_all('div', class_=re.compile('^(description)'))

    new_ad_num = 0
    for ad in ads:
        price_spam = ad.find('span', class_=re.compile('^(price)')).text

        try:
            price = int(''.join(filter(lambda x: x.isdigit(), price_spam)))
        except ValueError:
            price = 0

        a_info_ad = ad.find('a')
        data_ad = dict(zip(['title', 'link', 'price'],
                           [a_info_ad['title'], f'https://www.avito.ru/{a_info_ad["href"]}', price]))
        if ads_db.find_one({'link': data_ad['link']}) is None:
            ads_db.insert_one(data_ad)
            print('New record added')
            new_ad_num += 1
    print(f'{new_ad_num} new records added')



def find_in_mongo_db():

    price_max = int(input('какая максимальная цена для поиска? '))
    for ad in ads_db.find({'price': {'$gt' : 0, '$lte': price_max}}):
        pprint(ad)


# добавляет в пустую базу все найденные объявления
save_to_mongo_db()

# добавляет в базу только новые объявления
# save_only_new_to_mongo_db()

# ищет цены меньше введенной
# find_in_mongo_db()