import datetime
import requests
from bs4 import BeautifulSoup

weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

def get_html(url):
    response = requests.get(url).text
    return response

def parse(html):
    soup = BeautifulSoup(html, "lxml")
    days = []
    for block in soup.find_all('div', class_ = "forecast-briefly-old__day"):
        x = {}
        name = block.find('div', class_="forecast-briefly-old__name").get_text()
        if (name == "Сегодня"):
            x['name'] = weekdays[datetime.datetime.today().weekday()]
        else:
            x['name'] = name
        x['date'] = (block.find('time', class_="forecast-briefly-old__date").get_text())
        x['temp_day'] = (block.find('div', class_="forecast-briefly-old__temp_day").find('span', class_="temp__value").get_text())
        x['temp_night'] = (block.find('div', class_="forecast-briefly-old__temp_night").find('span', class_="temp__value").get_text())
        days.append(x)
    return days

def search(query):
    soup = BeautifulSoup(get_html("https://yandex.ru/pogoda/search?request="+query), "lxml")
    if (soup.find('div', class_="content").find('h1', class_="title title_level_1").get_text().lower() == "по вашему запросу ничего не нашлось"):
        return None
    element = soup.find('a', class_="link link_theme_normal place-list__item-name i-bem")
    if (element == None):
        return soup.find('head').find('link', rel="alternate")['href']
    else:
        return "https://yandex.ru" + element['href']

def getweather(town):
    if town == "":
        request = "https://yandex.ru/pogoda"
    else:
        request = search(town)
    if request == None:
        return None
    week = parse(get_html(request))
    return week

print(search("манила"))
