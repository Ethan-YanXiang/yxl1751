import requests
from bs4 import BeautifulSoup
from datetime import datetime
from data_collection.database import news_already_in_db, save_news_to_db, link_cluster_with_news
from data_collection.feature_engineering import save_corpus, train_and_save_tfidf_vectorizer, load_tfidf_vectorizer, body_to_vectors
from data_collection.unsupervised_machine_learning import real_time_single_pass_clustering
from fake_useragent import UserAgent
import random
import time

ua = UserAgent()


def format_date(date_text):
    parsed_date = datetime.strptime(date_text, '%a %d %b %Y %H.%M %Z')
    formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date


def fetch_article_data(article_url):
    time.sleep(random.uniform(1, 2))
    headers = {'User-Agent': ua.random}
    response = requests.get(article_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    try:
        maincontent = soup.find('div', class_='dcr-hm3fhj')
        paragraphs = maincontent.find_all('p')
        body = ' '.join(p.text.strip() for p in paragraphs)
        if len(body) == 0:
            return None
    except AttributeError:
        return None

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


def guardian_scraper():
    from full_stack_development.app import app

    headers = {'User-Agent': ua.random}
    response = requests.get('https://www.theguardian.com/uk', headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    with app.app_context():
        main_articles = soup.find_all('div', class_='dcr-4z6ajs')
        for main_article in main_articles:
            main_article_url = f'https://www.theguardian.com{main_article.a["href"]}'

            if news_already_in_db(main_article_url):
                print(f'{main_article_url} already in database')
                continue
            article_data = fetch_article_data(main_article_url)
            if article_data:
                headline, formatted_date, body, url = article_data
                article_id = save_news_to_db(headline, formatted_date, body, url)
                print(f'{headline} added to database')

                corpus = save_corpus(body)
                train_and_save_tfidf_vectorizer(corpus)
                tfidf_vectorizer = load_tfidf_vectorizer()
                tfidf_matrix, feature_names = body_to_vectors(body, tfidf_vectorizer)
                cluster_id = real_time_single_pass_clustering(tfidf_matrix, feature_names)
                link_cluster_with_news(article_id, cluster_id)

            sub_articles = main_article.find_all('li', class_='dcr-8x9syc')
            if sub_articles:
                for sub_article in sub_articles:
                    sub_article_url = f'https://www.theguardian.com{sub_article.a["href"]}'

                    if news_already_in_db(sub_article_url):
                        print(f'{sub_article_url} already in database')
                        continue
                    article_data = fetch_article_data(sub_article_url)
                    if article_data:
                        headline, formatted_date, body, url = article_data
                        article_id = save_news_to_db(headline, formatted_date, body, url)
                        print(f'{headline} added to database')

                        corpus = save_corpus(body)
                        train_and_save_tfidf_vectorizer(corpus)
                        tfidf_vectorizer = load_tfidf_vectorizer()
                        tfidf_matrix, feature_names = body_to_vectors(body, tfidf_vectorizer)
                        cluster_id = real_time_single_pass_clustering(tfidf_matrix, feature_names)
                        link_cluster_with_news(article_id, cluster_id)
