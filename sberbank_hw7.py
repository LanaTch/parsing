# Создать приложение, которое будет из готового файла с данными «Сбербанка»
# (https://www.sberbank.com/ru/analytics/opendata) выводить результат по параметрам:
# • Тип данных
# • Интервал дат
# • Область
# Визуализировать выводимые данные с помощью графика

import matplotlib.pyplot as plt
import pandas as pd

sber_df = pd.read_csv('opendata.csv', encoding='Windows-1251')
field_names = sber_df.columns
print(field_names)

type_data = input(f'какие данные показать? доступные данные: \n====\n{sber_df.name.unique()}\n?')
print('='*20)
region_data = input(f'какой регион? доступные регионы: \n====\n{sber_df.region.unique()}\n?')
dates_data = input(f'задайте интервал дат?\n минимальная дата: {sber_df.date.min()}'
                   f'\n максимальная дата: {sber_df.date.max()}'
                   f'\nвведите интервал в формате 2013-11-11,2014-11-11 ?')

date_min = dates_data.split(',')[0]
date_max = dates_data.split(',')[1]
total_df = sber_df.loc[(sber_df.name == type_data) &
                       (sber_df.region == region_data) &
                       (sber_df.date >= date_min) &
                       (sber_df.date <= date_max)]

plt.plot(total_df.date, total_df.value, 'go-')
plt.xlabel('дата')
plt.xticks(total_df.date, rotation='vertical')
plt.ylabel('руб.').set_rotation(90)
plt.title(f'{type_data} по {region_data}\nза период с {date_min} по {date_max}')
plt.grid()
plt.show()
