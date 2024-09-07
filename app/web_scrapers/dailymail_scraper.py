import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app.database.db import news_already_in_db, save_news_to_db
from app.feature_engineering import clean_text, body_to_vectors, save_corpus
from app.large_language_model.Ollama import llama3_sentiment
from app.machine_learning.single_pass_clustering import real_time_single_pass_clustering
from fake_useragent import UserAgent
import random
import time

ua = UserAgent()


def format_date(date_text):
    try:
        published_date = datetime.strptime(date_text, '%H:%M, %d %B %Y')
        return published_date
    except ValueError:
        return None


def fetch_article_data(article_url):
    time.sleep(random.uniform(0, 0.5))
    headers = {'User-Agent': ua.random}
    response = requests.get(article_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    try:
        headline = soup.h1.text.replace('EXCLUSIVE', '').replace('BREAKING NEWS', '').strip()
    except AttributeError:
        return None

    try:
        soup_ul_span = soup.find('p', class_='byline-section').find_all('span', class_='article-timestamp')
        formatted_date = None
        for i in soup_ul_span:
            date_text = i.text.strip()
            if 'Updated' in date_text:
                formatted_date = format_date(date_text.replace('Updated:', '').strip())
        if not formatted_date:
            formatted_date = format_date(soup_ul_span[0].text.replace('Published:', '').strip())
    except AttributeError:
        return None

    try:
        paragraphs = soup.find('div', itemprop='articleBody')
        body = ' '.join(p.text.strip() for p in paragraphs.find_all('p', class_='mol-para-with-font')).strip()
        if not body:
            print(f'failed to parse article {article_url}')
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
            sentiment = llama3_sentiment(article_url)  # when corpus
            tfidf_matrix, feature_names = body_to_vectors([clean_text(body)])
            cluster = real_time_single_pass_clustering(tfidf_matrix, feature_names)
            save_news_to_db(article_url, headline, formatted_date, body, sentiment, cluster)
            print(f'added article to db: {headline}')
        else:
            print(f'Failed to fetch all article data from: {article_url}')
    else:
        print(f'already in db: {article_url}')


def dailymail_scraper():

    headers = {'User-Agent': ua.random}
    response = requests.get('https://www.dailymail.co.uk', headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    articles = soup.find_all('h2', class_='linkro-darkred')

    for article in articles:
        article_url = article.a["href"]
        if not article_url.startswith('http'):
            article_url = 'https://www.dailymail.co.uk' + article_url

        process_article(article_url)
