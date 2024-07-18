from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.theguardian.com/uk').text
soup = BeautifulSoup(source, 'lxml')

articles = soup.find_all('div', class_='dcr-4z6ajs')
for article in articles:
    # print(article.prettify())

    try:
        headline = article.find('span', class_='show-underline dcr-1ch1h6j').text
        print(headline)
    except AttributeError:
        headline = None

    news_link = f'https://www.theguardian.com{article.a['href']}'
    print(news_link)

    print()

    sub_articles = article.find_all('li', class_='dcr-8x9syc')
    if sub_articles:
        for sub_article in sub_articles:
            try:
                sub_headline = sub_article.find('span', class_='show-underline dcr-1ch1h6j').text
                print(sub_headline)
            except AttributeError:
                sub_headline = None

            sub_news_link = f'https://www.theguardian.com{sub_article.a['href']}'
            print(sub_news_link)

            print()
