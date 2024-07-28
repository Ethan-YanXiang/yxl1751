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

    parsed_date = datetime.strptime(date_text, '%H:%M, %d %B %Y')
    formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date


def fetch_article_data(article_url):

    headers = {'User-Agent': ua.random}
    response = requests.get(article_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    try:
        maincontent = soup.find('div', itemprop='articleBody')
        paragraphs = maincontent.find_all('p', class_='mol-para-with-font')
        body = ' '.join(p.text.strip() for p in paragraphs)
    except AttributeError:
        body = None

    try:
        headline = soup.h1.text.strip()
    except AttributeError:
        headline = None

    try:
        formatted_date = format_date(soup.find('p', class_='byline-section').time.text.strip())
    except AttributeError:
        formatted_date = None

    return headline, formatted_date, body, article_url


count = 1


def dailymail_scraper():

    global count

    headers = {'User-Agent': ua.random}
    base_url = 'https://www.dailymail.co.uk'
    response = requests.get(base_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    articles = soup.find_all('h2', class_='linkro-darkred')
    for article in articles:
        article_url = article.a['href']
        if not article_url.startswith('http'):
            article_url = base_url + article_url
        if news_already_in_db(article_url):
            print(f'{article_url} is already in database')
            continue
        article_data = fetch_article_data(article_url)
        if article_data:
            save_news_to_db(article_data)
            print(f'news {count}: [{article_data[0]}] added to database')
            count += 1
            # time.sleep(random.uniform(1, 2))
            tfidf_matrix, feature_names = body_to_vectors(article_data[2])
            print(tfidf_matrix, feature_names)
