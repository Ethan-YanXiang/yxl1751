from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.theguardian.com/uk').text
soup = BeautifulSoup(source, 'lxml')

for article in soup.find_all('div', class_='dcr-4z6ajs'):
    # print(article.prettify())

    try:
        headline = article.find('span', class_='show-underline dcr-1ch1h6j').text
        print(headline)
    except AttributeError:
        headline = None

    news_link = f'https://www.theguardian.com{article.a['href']}'
    print(news_link)

    print()
