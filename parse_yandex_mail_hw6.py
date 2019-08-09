# 1) Написать программу, которая собирает входящие письма из своего
# или тестового почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма)

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient


def find_mails_and_add_to_db(links, db, driver):
    for i, link in enumerate(links, 1):
        driver.get(link)
        driver.implicitly_wait(10)
        time.sleep(3)
        mail_subject = driver.find_element_by_class_name('mail-Message-Toolbar-Subject-Wrapper').text
        mail_email = driver.find_element_by_xpath('//div[@class="mail-Message-Sender"]'
                                                  '/span[contains(@class, "Head")]/span').text
        mail_from_name = driver.find_element_by_xpath('//div[@class="mail-Message-Sender"]/span').text
        mail_date = driver.find_element_by_xpath('//div[contains(@class, "message-head-date")]').text
        mail_body = driver.find_element_by_xpath('//div[contains(@class,"mail-Message-Body-Content")]').text
        data_mail = dict(zip(['email', 'from_name', 'subject', 'date', 'body'],
                             [mail_email, mail_from_name, mail_subject, mail_date, mail_body]))
        db.insert_one(data_mail)
        print(f'{i} Record added')


client = MongoClient('mongodb://127.0.0.1:27017')
db_local = client['hw6']
yandex_db = db_local.yandex
yandex_db.drop()

driver_chrom = webdriver.Chrome()
driver_chrom.get('https://www.mail.yandex.ru/')
driver_chrom.implicitly_wait(10)  # максимальное время ожидания появление элементов на странице


# ищем и кликаем на кнопку Войти
elem = driver_chrom.find_element_by_xpath('//span[text()="Войти"]/parent::a')
elem.click()

# заполнение полей авторизации
# логин
elem = driver_chrom.find_element_by_id('passp-field-login')
elem.send_keys('bpb2')
elem.send_keys(Keys.RETURN)
# пароль
elem = driver_chrom.find_element_by_id('passp-field-passwd')
elem.send_keys('4580')
elem.send_keys(Keys.RETURN)

# поиск всех писем
mails_inbox = driver_chrom.find_elements_by_xpath('//div[@class="mail-MessageSnippet-Content"]/parent::a')
if len(mails_inbox) == 0:
    print('Нет писем в почте')

mails_links = [mail.get_attribute('href') for mail in mails_inbox]

find_mails_and_add_to_db(mails_links, yandex_db, driver_chrom)

driver_chrom.close()
