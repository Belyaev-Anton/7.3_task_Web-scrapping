from bs4 import BeautifulSoup
import requests
import re
import csv
from pprint import pprint

def f_all_news_in_page(box):
    f_list_all_news = []
    dict_found_news = {}
    for i in box:
        time_news = i.find('time').get('datetime')[:10]
        name_news = i.find('a', class_='tm-title__link').text
        link_news = url_mini + i.find('a', class_='tm-title__link').get('href')

        finish_line = time_news, name_news, link_news
        f_list_all_news.append(finish_line)
    return f_list_all_news

def f_regular_find_one_keywords(regular_keywords,regular_text):
    pattern = fr'(\b({regular_keywords})\b)'
    r = re.findall(pattern,regular_text,re.I)
    return r

def f_find_words_in_news(f_list_all_news, f_find_keywords, locator):
    f_list_found_news = []
    found_word = []
    index = 0
    for i in f_list_all_news:
        url = i[2]
        response = requests.get(url)
        content = response.text
        soup = BeautifulSoup(content, 'lxml')  # Задаем обьект soup
        box = soup.find('div', xmlns='http://www.w3.org/1999/xhtml')
        box_p = box.find_all('p')
        for element in box_p:
            text_box = element.text
            for word_find in f_find_keywords:
                if locator == 2:
                    res = f_regular_find_one_keywords(word_find.lower(),text_box.lower())
                    if  res != []:
                        if word_find not in found_word:
                            found_word.append(word_find)
                elif locator == 1:
                    if word_find.lower() in text_box.lower():
                        if word_find not in found_word:
                            found_word.append(word_find)
        dict_found_news = {
            "time_news": i[0],
            "name_news": i[1],
            "link_news": i[2],
            "found_word": found_word
        }
        found_word = []
        f_list_found_news.append(dict_found_news)

    return f_list_found_news

locator = int(input('1 - Поиск осущетвляется по заданной комбинации символов (дизайн == дизайнер == обдизайнерить)\n'
                    '2 - Поиск при помощи регулярки только одного заданного слова (дизайн != дизайнер != обдизайнерить)\n'))
find_keywords = ['дизайн', 'фото', 'web', 'python']
found_word = []
list_found_news = []
list_all_news = []

url = 'https://habr.com/ru/articles/page1/'
url_mini = 'https://habr.com'
response = requests.get(url)
content = response.text

soup = BeautifulSoup(content, 'lxml')       #Задаем обьект soup
box = soup.find_all('div', class_='tm-article-snippet tm-article-snippet')

list_all_news = f_all_news_in_page(box) #На заданной странице (по заданию) берем список статей: название, дата, ссылка
list_found_news = f_find_words_in_news(list_all_news, find_keywords,locator)

for b in list_found_news:
    j = b["found_word"]
    if b["found_word"] != []:
        print(f'{b["time_news"]} - {b["name_news"]} - {b["link_news"]} - {b["found_word"]} ')
