from bs4 import BeautifulSoup
import requests


def build_full_urls():
    source = requests.get('https://www.theguardian.com/uk').text
    soup = BeautifulSoup(source, 'lxml')

    '''construct full urls from all news page'''
    full_urls = []

    articles = soup.find_all('div', class_='dcr-4z6ajs')
    for article in articles:
        # print(article.prettify())

        # try:
        #     headline = article.find('span', class_='show-underline dcr-1ch1h6j').text
        # except AttributeError:
        #     headline = None
        # full_urls.append(headline)

        full_url = f'https://www.theguardian.com{article.a['href']}'
        full_urls.append(full_url)

        sub_articles = article.find_all('li', class_='dcr-8x9syc')
        if sub_articles:
            for sub_article in sub_articles:

                sub_full_url = f'https://www.theguardian.com{sub_article.a['href']}'
                full_urls.append(sub_full_url)

    return full_urls


# print(build_full_urls())
