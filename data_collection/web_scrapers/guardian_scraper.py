import requests
from bs4 import BeautifulSoup
from datetime import datetime
from data_collection.database import save_news_to_db, news_already_in_db
from data_collection.feature_engineering import body_to_vectors
from fake_useragent import UserAgent
import random
import time

ua = UserAgent()


def format_date(date_text):

    parsed_date = datetime.strptime(date_text, '%a %d %b %Y %H.%M %Z')
    formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date


def fetch_article_data(article_url):

    headers = {'User-Agent': ua.random}
    response = requests.get(article_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    try:
        maincontent = soup.find('div', class_='dcr-hm3fhj')
        paragraphs = maincontent.find_all('p')
        body = ' '.join(p.text.strip() for p in paragraphs)
        if len(body) == 0:
            return False
    except AttributeError:
        return False

    try:
        headline = soup.h1.text.strip()
    except AttributeError:
        headline = None

    try:
        formatted_date = format_date(soup.find('span', class_='dcr-u0h1qy').text.strip())
    except AttributeError:
        try:
            formatted_date = format_date(soup.find('div', class_='dcr-1pexjb9').text.strip())
        except AttributeError:
            formatted_date = None

    return headline, formatted_date, body, article_url


count = 1


def guardian_scraper():

    global count

    headers = {'User-Agent': ua.random}
    response = requests.get('https://www.theguardian.com/uk', headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    main_articles = soup.find_all('div', class_='dcr-4z6ajs')
    for main_article in main_articles:
        main_article_url = f'https://www.theguardian.com{main_article.a["href"]}'
        if news_already_in_db(main_article_url):
            print(f'{main_article_url} is already in database')
            continue
        main_article_data = fetch_article_data(main_article_url)
        if main_article_data:
            save_news_to_db(main_article_data)
            print(f'news {count}: {main_article_data[0]} added to database')
            count += 1
            # time.sleep(random.uniform(1, 2))
            tfidf_matrix, feature_names = body_to_vectors(main_article_data[2])
            print(tfidf_matrix, feature_names)

        sub_articles = main_article.find_all('li', class_='dcr-8x9syc')
        if sub_articles:
            for sub_article in sub_articles:
                sub_article_url = f'https://www.theguardian.com{sub_article.a["href"]}'
                if news_already_in_db(sub_article_url):
                    print(f'{sub_article_url} is already in database')
                    continue
                sub_article_data = fetch_article_data(sub_article_url)
                if sub_article_data:
                    save_news_to_db(sub_article_data)
                    print(f'news {count}: {sub_article_data[0]} added to database')
                    count += 1
                    # time.sleep(random.uniform(1, 2))
                    tfidf_matrix, feature_names = body_to_vectors(sub_article_data[2])
                    print(tfidf_matrix, feature_names)
