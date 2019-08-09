# Написать программу, которая собирает «Хиты продаж» с сайтов техники mvideo,
# onlinetrade и складывает данные в БД. Магазины можно выбрать свои.
# Главный критерий выбора: динамически загружаемые товары

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient


def find_hits_and_add_to_db(block, db):
    hits = block.find_elements_by_class_name('gallery-list-item')
    for hit in hits[:4]:
        hit_title = hit.find_element_by_tag_name('h4').get_attribute('title')
        print(hit_title)
        hit_link = hit.find_element_by_tag_name('a').get_attribute('href')
        print(hit_link)
        print('---')
        data_hit = dict(zip(['title', 'link'],
                            [hit_title, hit_link]))
        db.insert_one(data_hit)
        print('Record added')
        print('===')


CLIENT = MongoClient('mongodb://127.0.0.1:27017')
DB = CLIENT['hw6']
MVIDEO_DB = DB.mvideo
MVIDEO_DB.drop()

driver = webdriver.Chrome()
driver.get("https://www.mvideo.ru/")
driver.implicitly_wait(10)  # максимальное время ожидания появление элементов на странице

# тк кнопка прокрутки страниц "хиты продаж" появляется только при наведении курсора
# на блок. наводим и держим
block_hits = driver.find_element_by_xpath('//div[contains(text(), "Хиты продаж")]'
                                          '/following::ul[@class="accessories-product-list"]')
ActionChains(driver).move_to_element(block_hits).release().perform()
next_btn = driver.find_element_by_xpath('//div[contains(text(), "Хиты продаж")]/'
                                        'following::a[@class="next-btn sel-hits-button-next"]')

find_hits_and_add_to_db(block_hits, MVIDEO_DB)
for _ in range(3):
    next_btn.click()
    time.sleep(3)  # надо, чтобы после прокрутки списка хитов успело обновится содержание элементов
    find_hits_and_add_to_db(block_hits, MVIDEO_DB)

driver.close()
