import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# https://v1.ru/

client = MongoClient()
db = client.news_parser
news_coll = db.news

def getHtml(url):
    r = requests.get(url)
    return r.text

def getNews(html):
    soup = BeautifulSoup(html, 'lxml')
    news = soup.findAll('article', class_='MFa0x')
    newTexts = ""
    for i in range(len(news)):
        Name = news[i].find('h2', class_='MFdp').find('a').text
        Link = 'https://v1.ru' + news[i].find('h2', class_='MFdp').find('a').get('href')
        if Link == 'https://v1.ruhttps://v1.ru/text/longread/food/69502387/':
            continue
        Date = news[i].find('time').get('datetime')
        Views = news[i].find('div', class_='LVlh').find('span').text.replace("\xa0", "")
        if len(news[i].find('div', class_='LVayr').findAll('span', class_='LVjt')) > 1:
            if news[i].find('div', class_='LVayr').findAll('span', class_='LVjt')[1].text == " Обсудить ":
                Comments = "0"
            else:
                Comments = news[i].find('div', class_='LVayr').findAll('span', class_='LVjt')[1].text
        else:
            Comments = "0"

        verify = news_coll.find_one({'Name news': Name})

        if not(str(verify) == 'None'):
            for new in news_coll.find():
                if new['Name news'] == Name:
                    new['Views news'] = Views
                    new['Comments news'] = Comments
        else:
            soup2 = BeautifulSoup(getHtml(Link), 'lxml')
            blocks = soup2.findAll('div', class_='LNaxf')
            for k in range(len(blocks)):
                texts = blocks[k].findAll('p')
                for r in range(len(texts)):
                    newTexts += texts[r].text + '\n'
            Text = newTexts
            newTexts = ""

            news_doc = {
                "Name news": Name,
                "Date news": Date,
                "Link news": Link,
                "Text news": Text,
                "Views news": Views,
                "Comments news": Comments
            }
            news_coll.insert_one(news_doc)

url = "https://v1.ru/text/"

getNews(getHtml(url))





