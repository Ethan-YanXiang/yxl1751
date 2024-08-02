import requests
from bs4 import BeautifulSoup
from datetime import datetime
import concurrent.futures
from data_collection.database import save_news_to_db, news_already_in_db
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


def process_article(article_url):
    if news_already_in_db(article_url):
        print(f'{article_url} already in database')
        return None
    article_data = fetch_article_data(article_url)
    if article_data:
        headline, formatted_date, body, url = article_data
        save_news_to_db(headline, formatted_date, body, url)
        print(f'{headline} added to database')
        return body
    return None


def guardian_scraper():
    bodies = []

    headers = {'User-Agent': ua.random}
    response = requests.get('https://www.theguardian.com/uk', headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

        futures = []

        main_articles = soup.find_all('div', class_='dcr-4z6ajs')
        for main_article in main_articles:
            main_article_url = f'https://www.theguardian.com{main_article.a["href"]}'
            futures.append(executor.submit(process_article, main_article_url))

            sub_articles = main_article.find_all('li', class_='dcr-8x9syc')
            if sub_articles:
                for sub_article in sub_articles:
                    sub_article_url = f'https://www.theguardian.com{sub_article.a["href"]}'
                    futures.append(executor.submit(process_article, sub_article_url))

        for future in concurrent.futures.as_completed(futures):
            body = future.result()
            if body:
                bodies.append(body)

    return bodies
