import requests
from bs4 import BeautifulSoup
from datetime import datetime
from data_collection.database import news_already_in_db, save_news_to_db, link_cluster_with_news
from data_collection.feature_engineering import save_corpus, body_to_vectors
from data_collection.unsupervised_machine_learning import real_time_single_pass_clustering
from fake_useragent import UserAgent
import random
import time

ua = UserAgent()
base_url = 'https://www.dailymail.co.uk'


def format_date(date_text):
    parsed_date = datetime.strptime(date_text, '%H:%M, %d %B %Y')
    formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date


def fetch_article_data(article_url):
    # time.sleep(random.uniform(0, 1))
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


def dailymail_scraper():
    from full_stack_development.app import app

    headers = {'User-Agent': ua.random}
    response = requests.get(base_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    with app.app_context():
        articles = soup.find_all('h2', class_='linkro-darkred')
        for article in articles:
            article_url = article.a['href']
            if not article_url.startswith('http'):
                article_url = base_url + article_url

            if news_already_in_db(article_url):
                print(f'{article_url} already in database')
                continue
            article_data = fetch_article_data(article_url)
            if article_data:
                headline, formatted_date, body, url = article_data
                article_id = save_news_to_db(headline, formatted_date, body, url)
                print(f'{headline} added to database')

                # save_corpus(body)
                tfidf_matrix, feature_names = body_to_vectors(body)
                cluster_id = real_time_single_pass_clustering(tfidf_matrix, feature_names)
                link_cluster_with_news(article_id, cluster_id)
