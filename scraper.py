import requests
from bs4 import BeautifulSoup
import string
from os.path import exists
from os import mkdir


def not_imdb(url):
    if 'imdb' in url and 'title' in url:
        return False
    return True


def get_imdb(url, english=False):
    if not_imdb(url):
        print("Invalid movie page!")
        return
    if english:
        r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    else:
        r = requests.get(url)

    if r.status_code != 200:
        print("Invalid movie page!")
    else:
        data = {}
        soup = BeautifulSoup(r.content, 'html.parser')
        data["title"] = soup.find('h1').text
        dis = soup.find('span', {'role': "presentation", "data-testid": "plot-l"})
        if dis:
            data["description"] = dis.text
        print(data)


def save_page(url, file_name=None, page_n=None):
    r = requests.get(url)

    if r.status_code != 200:
        print('The URL returned ' + str(r.status_code) + '!')
    else:
        dir = ''
        if page_n:
            dir = 'Page_' + str(page_n) + '/'

        if file_name:
            file_name = file_name.translate(str.maketrans('', '', string.punctuation))\
                            .strip().replace('-', '').replace(' ', '_') + '.txt'
        else:
            file_name = 'source.html'
        soup = BeautifulSoup(r.content, 'html.parser')
        with open(dir + file_name, 'wb') as source:
            source.write(soup.find('div', {'class': 'c-article-body'}).text.encode('UTF-8'))
        # print('Content saved in file ' + file_name + '.')
        return file_name


def get_url_content():
    url = input("Input the URL:\n")
    get_imdb(url, english=True)


def scrap_page(url, num=None, type_article=None):

    if num:
        for i in range(1, num + 1):
            if not(exists('Page_' + str(i))):
                mkdir('Page_' + str(i))
    r = requests.get(url)

    if r.status_code != 200:
        print('The URL returned ' + str(r.status_code) + '!')
    else:
        data = {}
        soup = BeautifulSoup(r.content, 'html.parser')
        all_articles = soup.find_all('article',
                                    {'itemtype': "http://schema.org/ScholarlyArticle"})

        files_names = []
        for article in all_articles:
            if article.find_all('span', text=type_article):
                a = article.find('a', {'data-track-action': "view article"})
                files_names.append(save_page('https://www.nature.com' + a['href'], a.text, num))
        print("Saved articles:")
        print(files_names)


def scrap_n_pages(num_pages=None, type_article=None):
    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='

    for i in range(1, num_pages + 1):
        scrap_page(url + str(i), i, type_article)
    pass


num_of_pages = int(input())
type_article = input()
scrap_n_pages(num_of_pages, type_article)
