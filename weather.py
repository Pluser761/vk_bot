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
        x['temp'] = (block.find('span', class_="temp__value").get_text())
        days.append(x)
    return days

def search(query):
    soup = BeautifulSoup(get_html("https://yandex.ru/pogoda/search?request="+query), "lxml")
    elements = soup.find_all('a', class_="link link_theme_normal place-list__item-name i-bem")
    for element in elements:
        if element.get_text().lower() == query.lower():
            return "https://yandex.ru" + element['href']

def getweathertown(town):
    town.lower()
    request = search(town)
    week = parse(get_html(request))
    return week

def getweather():
    request = "https://yandex.ru/pogoda/moscow"
    week = parse(get_html(request))
    return week

print(getweathertown("тула"))
