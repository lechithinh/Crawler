from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random

url_base = 'https://dl.acm.org/action'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en,vi-VN;q=0.9,vi;q=0.8,fr-FR;q=0.7,fr;q=0.6,en-US;q=0.5',
    'Connection': 'keep-alive'
}
params = {
    'startPage': '0',
    'pageSize': '20'
}


def GetPageContent(url):
    respone = requests.get(url, headers=headers, params=params)
    if respone.status_code == 200:
        print('Request success')
        soup = BeautifulSoup(respone.content, 'html.parser')
        return soup


def getLinkPaper():
    lst_link = []
    url = url_search
    soup = GetPageContent(url)
    src = soup.find_all('span', class_='hlFld-Title')
    for paper_link in src:
        link = paper_link.find('a').get('href')
        lst_link.append(url_base + link)
    return lst_link


result = []


def CrawlDataPaper():
    lst_link = getLinkPaper()
    for link in lst_link:
        d = dict()
        lst_authors = []
        # lst_reference = []
        soup = GetPageContent(link)
        authors = soup.find_all('li', class_='loa__item')
        for author in authors:
            lst_authors.append(author.find('a').get('title'))
        if name_author in lst_authors:
            d['Content_Paper'] = soup.find('h1', class_='citation__title').text
            d['Link_Paper'] = link
            d['Authors'] = lst_authors
            d['Public_time'] = soup.find(
                'span', class_='epub-section__date').text
            d['Public_Location'] = soup.find(
                'span', class_='epub-section__title').text
            references = soup.find_all('span', class_='references__note')
        else:
            continue
        result.append(d)


name_author = input('Input name author to find paper:')
url_search = url_base + '/doSearch?AllField=' + \
    str(name_author).replace(' ', '+')
for i in range(0, 5):
    params['startPage'] = i
    respone = requests.get(url_search, headers=headers, params=params)
    if respone.status_code == 200:
        CrawlDataPaper()
    time.sleep(random.randrange(3, 10))

df = pd.DataFrame(result)
df.to_csv('paperofauthor.csv', index=False)
