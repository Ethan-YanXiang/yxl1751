import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app.database.db import news_already_in_db, save_news_to_db, link_cluster_in_db
from app.feature_engineering.data_cleaning import clean_text
from app.feature_engineering.tfidf_vectorizer import body_to_vectors, save_corpus
from app.machine_learning.single_pass_clustering import real_time_single_pass_clustering
from fake_useragent import UserAgent
import random
import time

ua = UserAgent()


def format_date(date_text):
    parsed_date = datetime.strptime(date_text, '%a %d %b %Y %H.%M %Z')
    published_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
    return published_date



def fetch_article_data(article_url):
    time.sleep(random.uniform(0, 1.5))
    headers = {'User-Agent': ua.random}
    response = requests.get(article_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    try:
        headline = soup.h1.text.strip()
    except AttributeError:
        return None

    try:
        date_text = soup.find('span', class_='dcr-u0h1qy').text.strip()
        published_date = format_date(date_text)
    except AttributeError:
        try:
            date_text = soup.find('div', class_='dcr-1pexjb9').text.strip()
            published_date = format_date(date_text)
        except AttributeError:
            return None

    try:
        maincontent = soup.find('div', id='maincontent')
        paragraphs = maincontent.find_all('p')
        body = ' '.join(p.text.strip() for p in paragraphs)
        if len(body) == 0:
            return None
    except AttributeError:
        return None

    return headline, published_date, body


def process_article(article_url):
    if news_already_in_db(article_url):
        print(f'already in db: {article_url}\n')
        return
    # save_news_to_db(article_url)
    article_data = fetch_article_data(article_url)
    if article_data is None:
        print(f'Failed to fetch all article data from: {article_url}\n')
        return

    headline, published_date, body = article_data
    # save_corpus(clean_text(body))
    article_id = save_news_to_db(article_url, headline, published_date, body)  # when corpus
    print(f'Added {article_id} article to db: {headline}')
    tfidf_matrix, feature_names = body_to_vectors(clean_text(body))
    cluster_id = real_time_single_pass_clustering(tfidf_matrix, feature_names)
    link_cluster_in_db(article_id, cluster_id)


def guardian_scraper():

    headers = {'User-Agent': ua.random}
    response = requests.get('https://www.theguardian.com/uk', headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    main_articles = soup.find_all('div', class_='dcr-4z6ajs')
    for main_article in main_articles:
        main_article_url = f'https://www.theguardian.com{main_article.a["href"]}'
        process_article(main_article_url)

        sub_articles = main_article.find_all('li', class_='dcr-8x9syc')
        if sub_articles:
            for sub_article in sub_articles:
                sub_article_url = f'https://www.theguardian.com{sub_article.a["href"]}'
                process_article(sub_article_url)
