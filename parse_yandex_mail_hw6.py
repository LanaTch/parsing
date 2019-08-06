# 1) Написать программу, которая собирает входящие письма из своего
# или тестового почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма)
from selenium import common
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient



def find_mails_and_add_to_db(mails, db, driver):
    for i in range(len(mails)):
        mail_fromtext = mails[i].find_element_by_class_name('mail-MessageSnippet-FromText')
        mail_email = mail_fromtext.get_attribute('title')
        mail_from_name = mail_fromtext.text

        mail_subject = mails[i].find_element_by_css_selector('.mail-MessageSnippet-Item'
                                                             '.mail-MessageSnippet-Item_subject').text
        mail_date = mails[i].find_element_by_class_name('mail-MessageSnippet-Item_dateText').get_attribute('title')

        mails[i].click()
        try:
            mail_body = driver.find_element_by_tag_name('tbody').text
        except common.exceptions.NoSuchElementException:
            mail_body = driver.find_element_by_class_name('mail-Message-Body-Content').text
        finally:
            data_mail = dict(zip(['email', 'from_name', 'subject', 'date', 'body'],
                                 [mail_email, mail_from_name, mail_subject, mail_date, mail_body]))
            db.insert_one(data_mail)
            print(f'{i + 1} Record added')

            driver.back()  # возврат на страницу с письмами
            # снова ищем письма т к открывали другую страницу
            mails = driver.find_elements_by_class_name('mail-MessageSnippet-Content')


client = MongoClient('mongodb://127.0.0.1:27017')
db_local = client['hw6']
yandex_db = db_local.yandex
yandex_db.drop()

driver_chrom = webdriver.Chrome()
driver_chrom.get('https://www.mail.yandex.ru/')
driver_chrom.implicitly_wait(10) # максимальное время ожидания появление элементов на странице


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
mails_inbox = driver_chrom.find_elements_by_class_name('mail-MessageSnippet-Content')

find_mails_and_add_to_db(mails_inbox, yandex_db, driver_chrom)

driver_chrom.close()