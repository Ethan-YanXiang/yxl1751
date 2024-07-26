import requests
from bs4 import BeautifulSoup
import random
import time
from fake_useragent import UserAgent
from datetime import datetime
from web_scrapers.db import save_news_to_db, news_already_in_db

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
        body = ' '.join(p.text for p in paragraphs)
    except AttributeError:
        body = None

    try:
        headline = soup.h1.text
    except AttributeError:
        headline = None

    try:
        formatted_date = format_date(soup.find('p', class_='byline-section').time.text.strip())
    except AttributeError:
        formatted_date = None

    return headline, formatted_date, body, article_url


def crawl_dailymail():

    headers = {'User-Agent': ua.random}
    base_url = 'https://www.dailymail.co.uk'
    response = requests.get(base_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    articles = soup.find_all('h2', class_='linkro-darkred')
    for article in articles:
        article_url = article.a['href']
        if not article_url.startswith('http'):
            article_url = base_url + article_url
        if not news_already_in_db(article_url):
            article_data = fetch_article_data(article_url)
            if article_data:
                save_news_to_db(article_data)
                time.sleep(random.uniform(1, 2))
        # print_article_data(article_url)


# def print_article_data(article_url):
#
#     article_data = fetch_article_data(article_url)
#     if article_data:
#         headline, formatted_date, body, article_url = article_data
#         print(f"Headline: {headline}")
#         print(f"Date: {formatted_date}")
#         print(f"Body: {body}")
#         print(f"URL: {article_url}\n")


if __name__ == '__main__':
    crawl_dailymail()
