import requests
from bs4 import BeautifulSoup
from datetime import datetime
import concurrent.futures
from data_collection.database import save_news_to_db, news_already_in_db
from data_collection.feature_engineering import train_and_save_tfidf_vectorizer, body_to_vectors
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
    time.sleep(random.uniform(1, 2))
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


def process_article(article):
    article_url = article.a['href']
    if not article_url.startswith('http'):
        article_url = base_url + article_url

    if news_already_in_db(article_url):
        print(f'{article_url} already in database')
        return None
    article_data = fetch_article_data(article_url)
    if article_data:
        save_news_to_db(article_data)
        print(f'{article_data[0]} added to database')
        return article_data[2]
    return None


def dailymail_scraper():
    bodies = []

    headers = {'User-Agent': ua.random}
    response = requests.get(base_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        articles = soup.find_all('h2', class_='linkro-darkred')
        futures = [executor.submit(process_article, article) for article in articles]

        for future in concurrent.futures.as_completed(futures):
            body = future.result()
            if body:
                bodies.append(body)

    if bodies:
        tfidf_vectorizer = train_and_save_tfidf_vectorizer(bodies)
        for body in bodies:
            tfidf_matrix, feature_names = body_to_vectors(body, tfidf_vectorizer)
            clusters, cluster_keywords = real_time_single_pass_clustering(tfidf_matrix)
            print(f'{clusters} clusters and {cluster_keywords}')
