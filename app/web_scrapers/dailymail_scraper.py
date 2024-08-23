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
base_url = 'https://www.dailymail.co.uk'


def format_date(date_text):
    parsed_date = datetime.strptime(date_text, '%H:%M, %d %B %Y')
    published_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
    return published_date


def fetch_article_data(article_url):
    time.sleep(random.uniform(0, 1))
    headers = {'User-Agent': ua.random}
    response = requests.get(article_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    try:
        maincontent = soup.find('div', itemprop='articleBody')
        paragraphs = maincontent.find_all('p', class_='mol-para-with-font')
        body = ' '.join(p.text.strip() for p in paragraphs)
        cleaned_body = clean_text(body)

    except AttributeError:
        return None, None

    try:
        headline = soup.h1.text.strip()
    except AttributeError:
        return None, None

    try:
        date_text = soup.find('p', class_='byline-section').time.text.strip()
        published_date = format_date(date_text)
    except AttributeError:
        return None, None

    article_id = save_news_to_db(article_url)
    # article_id = save_news_to_db(headline, published_date, body, article_url)  # when corpus
    print(f'added {article_id} article to db: {headline}')
    return cleaned_body, article_id


def process_article(article_url):
    if news_already_in_db(article_url):
        print(f'already in db: {article_url}')
        return

    cleaned_body, article_id = fetch_article_data(article_url)
    if cleaned_body and article_id:

        save_corpus(cleaned_body)
        # tfidf_matrix, feature_names = body_to_vectors(cleaned_body)  # when corpus
        # print(f'tfidf_matrix:\n{tfidf_matrix}')
        # cluster_id = real_time_single_pass_clustering(tfidf_matrix, feature_names)
        # link_cluster_in_db(article_id, cluster_id)
        # print(f'{article_id} articles : {cluster_id} clusters')


def dailymail_scraper():

    headers = {'User-Agent': ua.random}
    response = requests.get(base_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    articles = soup.find_all('h2', class_='linkro-darkred')

    for article in articles:
        article_url = article.a['href']
        if not article_url.startswith('http'):
            article_url = base_url + article_url

        process_article(article_url)
