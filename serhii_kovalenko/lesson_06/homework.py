# Создать консольную программу-парсер, с выводом прогноза погоды. Дать возможность пользователю получить
# прогноз погоды в его локации ( по умолчанию) и в выбраной локации, на определенную пользователем дату.
# Можно реализовать, как консольную программу, так и веб страницу. Используемые инструменты: requests, beatifulsoup,
# остальное по желанию. На выбор можно спарсить страницу, либо же использовать какой-либо API


from bs4 import BeautifulSoup as bs
import requests
import datetime


city = input('Please enter your city: ')
date = input('Please enter date (example: 29.10.2019): ')

date = datetime.datetime.strptime('29.10.2019', '%d.%m.%Y')
today = datetime.datetime.strptime(str(datetime.datetime.now())[0:10], '%Y-%m-%d')
date_diff_day = date - today

convert_date_input = str(f'{date.year}-{date.month}-{date.day}')

url = f'https://sinoptik.ua/погода-{city}/{convert_date_input}'
page = requests.get(url)
soup = bs(page.text, 'html.parser')

if date_diff_day.days < 2:
    print(f'''{soup.find_all(class_="description")[0].get_text()}
    Ночью: {soup.find_all(class_="p1")[2].get_text()}
    Утром: {soup.find_all(class_="p3")[2].get_text()}
    Днем: {soup.find_all(class_="p5")[2].get_text()}
    Вечером: {soup.find_all(class_="p7")[2].get_text()}
''')
else:
    print(f'''{soup.find_all(class_="description")[0].get_text()}
    ночью: {soup.find_all(class_="p1 bR")[2].get_text()}
    утром: {soup.find_all(class_="p2 bR")[2].get_text()}
    днем: {soup.find_all(class_="p3 bR")[2].get_text()}
    вечером: {soup.find_all(class_="p4")[2].get_text()}
''')
