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

        full_url = f'https://www.theguardian.com{article.a['href']}'
        full_urls.append(full_url)

        sub_articles = article.find_all('li', class_='dcr-8x9syc')
        if sub_articles:
            for sub_article in sub_articles:

                sub_full_url = f'https://www.theguardian.com{sub_article.a['href']}'
                full_urls.append(sub_full_url)

    return full_urls


# print(build_full_urls())


def extract_articles(full_urls):

    full_articles = ''

    for full_url in full_urls:
        source = requests.get(full_url).text
        soup = BeautifulSoup(source, 'lxml')

        '''construct full articles for all urls'''

        headline = soup.h1.text
        full_articles += f'{headline}\n'

        try:
            sub_headline = soup.find('div', style='--grid-area:standfirst;').p.text
        except AttributeError:
            sub_headline = 'None'
        full_articles += f'{sub_headline}\n'

        try:
            body = soup.find('div', id='maincontent').get_text(separator='', strip=True)
        except AttributeError:
            body = 'None'
        full_articles += f'{body}\n\n'

    return full_articles


print(extract_articles(build_full_urls()))
