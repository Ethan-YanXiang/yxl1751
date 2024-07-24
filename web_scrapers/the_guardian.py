import requests
from bs4 import BeautifulSoup


def fetch_article_data(article_url):

    response = requests.get(article_url).text
    soup = BeautifulSoup(response, 'lxml')

    try:
        body = soup.find('div', class_='dcr-1qg0p6f').get_text(separator='', strip=True)
        if len(body) == 0:
            return False
    except AttributeError:
        return False

    try:
        headline = soup.h1.text.strip()
    except AttributeError:
        headline = None

    try:
        date = soup.find('span', class_='dcr-u0h1qy').text
    except AttributeError:
        try:
            date = soup.find('div', class_='dcr-1pexjb9').text
        except AttributeError:
            date = None

    return headline, date, body, article_url


def build_full_urls():
    response = requests.get('https://www.theguardian.com/uk').text
    soup = BeautifulSoup(response, 'lxml')

    main_articles = soup.find_all('div', class_='dcr-4z6ajs')
    for main_article in main_articles:
        main_article_url = f'https://www.theguardian.com{main_article.a['href']}'
        fetch_article_data(main_article_url)
        # print_article_data(main_article_url)

        sub_articles = main_article.find_all('li', class_='dcr-8x9syc')
        if sub_articles:
            for sub_article in sub_articles:
                sub_article_url = f'https://www.theguardian.com{sub_article.a['href']}'
                fetch_article_data(sub_article_url)
                # print_article_data(sub_article_url)


# def print_article_data(article_url):
#     if fetch_article_data(article_url):
#         headline, date, body, article_url = fetch_article_data(article_url)
#         print(f"Headline: {headline}")
#         print(f"Date: {date}")
#         print(f"Body: {body}")
#         print(f"URL: {article_url}\n")


build_full_urls()
