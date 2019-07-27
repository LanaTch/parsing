# Необходимо собрать информацию о вакансиях на должность программиста или разработчика
# с сайта job.ru или hh.ru. (Можно с обоих сразу) Приложение должно анализировать
# несколько страниц сайта. Получившийся список должен содержать в себе:
#
# *Наименование вакансии,
# *Предлагаемую зарплату
# *Ссылку на саму вакансию
#  Доработать приложение таким образом, чтобы можно было искать разработчиков
#  на разные языки программирования (Например Python, Java, C++)

import requests
from lxml import html
from pprint import pprint
import pandas as pd

pd.options.display.max_columns = 4

def return_html_from_url(url, param_hh):
    # функция по url позвращает html страницы по запросу

    headers_hh = {'accept':'*/&*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    session_hh = requests.session()
    hh_request = session_hh.get(url,
                                params=param_hh,
                                headers=headers_hh)

    return hh_request.text


def find_vacancies_headers(html_page):
    # функция ищет в html заголовок с названием вакансии, ссылкой на нее и зарплатой

    v_ = html.fromstring(html_page).xpath('//a[contains(@class, "bloko-link HH-LinkModifier")]')
    s_ = html.fromstring(html_page).xpath\
        ('//div[contains(@class, "vacancy-serp-item__row vacancy-serp-item__row_header")]'
         '/div[contains(@class, "vacancy-serp-item__sidebar")]')

    return (v_, s_)


def find_last_page(html_page):
    # функция ищет количество страниц с вакансиями (последнее поле в списке страниц)

    last_page_str = html.fromstring(html_page).xpath \
            ('//div[@data-qa="pager-block"]/*/a[@class="bloko-button HH-Pager-Control"]')

    last_page = int(last_page_str[0].text_content()) if len(last_page_str) > 0 else 1

    return last_page


if __name__ == '__main__':

    search_vacancy = input('какую вакансию искать?  ')

    vacancies_list = []
    last_page = 1 # хотя бы 1 страница с вакансиями будет
    i = 0
    while i < last_page:
        param_search = {'text': search_vacancy,
                        'area': '1',
                        'page': str(i)}

        hh_html = return_html_from_url(f'https://hh.ru/search/vacancy', param_search)

        if i == 0:
            max_pages = find_last_page(hh_html)
            print(f'всего {max_pages} страниц с вакансиями "{search_vacancy}"')
            last_page = int(input(f'сколько страниц просмотреть (максимум {max_pages})? '))
            print('подождите, идет поиск...')

        vacancies, salaries = find_vacancies_headers(hh_html)

        # добавляем вакансии с текущей страницы в итоговый список
        for v, s in zip(vacancies, salaries):
            vacancies_dict = {}
            vacancies_dict['name'] = v.text_content()
            vacancies_dict['url'] = v.get('href').split('?')[0]
            vacancies_dict['salary'] = s.text_content() if len(s.text_content()) > 0 \
                else 'зарплата не указана'
            vacancies_list.append(vacancies_dict)

        i+=1

    print(f'найдено {len(vacancies_list)} вакансий')

    max_pos = int(input(f'сколько вакансий вывести на экран?   '))

    pprint(pd.DataFrame(vacancies_list[:max_pos]))