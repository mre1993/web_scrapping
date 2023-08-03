
import requests
from bs4 import BeautifulSoup
import sqlite3
page = requests.get(r'https://www.iranjib.ir/showarchive/0/0/')
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find_all('table', {'class':'cellpadding5'})

links_a = table[0].find_all('a')
links_href = []
for item in links_a:
    links_href.append(item.get('href'))
    print(links_href)
con = sqlite3.connect('iranjib.db')
cur = con.cursor()
statement = """ CREATE TABLE IF NOT EXISTS News(
                id INTEGER,
                title TEXT,
                date TEXT,
                shortDescription TEXT,
                link TEXT
                            )"""
cur.execute(statement)
id = 0
for url in links_href:
    id += 1
    each_news = requests.get(url)
    news_item = []
    news_item.append(id)
    each_news_soup = BeautifulSoup(each_news.content, "html.parser")
    title = each_news_soup.find_all('h1', {"class":"titlenas"})
    news_item.append(title[0].get_text())
    date = each_news_soup.find_all('td', {"style":"width:60%"})
    news_item.append(date[0].get_text())
    shortDescription = each_news_soup.find_all('div', {"class":"newssummary"})
    news_item.append(shortDescription[0].get_text())
    news_item.append(url)
    statement = """ INSERT INTO News VALUES (?,?,?,?,?)"""
    cur.execute(statement, news_item)
    con.commit()
con.close()    