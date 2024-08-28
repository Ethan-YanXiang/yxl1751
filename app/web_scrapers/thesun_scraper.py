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
    try:
        parsed_date = datetime.strptime(date_text, '%H:%M, %d %b %Y')
        formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_date
    except ValueError:
        return None


def fetch_article_data(article_url):
    time.sleep(random.uniform(0, 1))
    headers = {'User-Agent': ua.random}
    response = requests.get(article_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    try:
        headline = soup.h1.text.strip()
    except AttributeError:
        return None

    try:
        soup_ul_time = soup.find('ul', class_='article__time').find_all('time')
        formatted_date = None
        for i in soup_ul_time:
            date_text = i.text.strip()
            if 'Updated' in date_text:
                formatted_date = format_date(date_text.replace('Updated: ', '').strip())
                print(f'updated date: {formatted_date}')
        if not formatted_date:
            formatted_date = format_date(soup_ul_time[0].text.replace('Published: ', '').strip())
            print(f'original date: {formatted_date}')
    except AttributeError:
        return None

    try:
        soup_div_p = soup.find('div', class_='article__content').find_all('p')
        body = ' '.join(p.text.strip() for p in soup_div_p).strip()
        if not body:
            return None
    except AttributeError:
        return None

    return headline, formatted_date, body


def process_article(article_url):
    if not news_already_in_db(article_url):
        article_data = fetch_article_data(article_url)

        if article_data:
            headline, formatted_date, body = article_data
            # save_news_to_db(article_url)
            # save_corpus(clean_text(body))
            article_id = save_news_to_db(article_url, headline, formatted_date, body)  # when corpus
            print(f'added {article_id} article to db: {headline}')
            tfidf_matrix, feature_names = body_to_vectors(clean_text(body))
            cluster_id = real_time_single_pass_clustering(tfidf_matrix, feature_names)
            link_cluster_in_db(article_id, cluster_id)
        else:
            print(f'Failed to fetch all article data from: {article_url}')
    else:
        print(f'already in db: {article_url}')


def thesun_scraper():

    headers = {'User-Agent': ua.random}
    response = requests.get('https://www.thesun.co.uk', headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    articles = soup.find_all('div', class_='col')

    for article in articles:
        a_tag = article.find('a')
        if a_tag and 'href' in a_tag.attrs:
            article_url = a_tag['href']
            process_article(article_url)
