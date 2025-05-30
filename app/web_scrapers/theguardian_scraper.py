import random
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from app.database.db import news_already_in_db, save_news_to_db
from app.feature_engineering import body_to_vectors, clean_text, save_corpus
from app.large_language_model.Ollama import llama3_sentiment
from app.machine_learning.single_pass_clustering import real_time_single_pass_clustering

ua = UserAgent()


def format_date(date_text):
    try:
        formatted_date = datetime.strptime(
            date_text.replace(" BST", ""), "%a %d %b %Y %H.%M"
        )
        return formatted_date
    except ValueError:
        return None


def fetch_article_data(article_url):
    time.sleep(random.uniform(0, 1.5))
    headers = {"User-Agent": ua.random}
    response = requests.get(article_url, headers=headers).text
    soup = BeautifulSoup(response, "lxml")

    try:
        headline = soup.h1.text.strip()
    except AttributeError:
        return None

    try:
        date_text = soup.find("span", class_="dcr-u0h1qy").text.strip()
        formatted_date = format_date(date_text)
    except AttributeError:
        try:
            date_text = soup.find("div", class_="dcr-1pexjb9").text.strip()
            formatted_date = format_date(date_text)
        except AttributeError:
            return None

    try:
        paragraphs = soup.find_all("p", class_="dcr-16w5gq9")
        body = " ".join(p.text.strip() for p in paragraphs).strip()
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
            sentiment = llama3_sentiment(article_url)  # when corpus
            tfidf_matrix, feature_names = body_to_vectors([clean_text(body)])
            cluster = real_time_single_pass_clustering(tfidf_matrix, feature_names)
            save_news_to_db(
                article_url, headline, formatted_date, body, sentiment, cluster
            )
            print(f"Added article to db: {headline}")
        else:
            print(f"Failed to fetch all article data from: {article_url}")
    else:
        print(f"already in db: {article_url}")


def theguardian_scraper():

    headers = {"User-Agent": ua.random}
    response = requests.get("https://www.theguardian.com/uk", headers=headers).text
    soup = (
        BeautifulSoup(response, "lxml")
        .find("main", id="maincontent")
        .find_all("div", class_=["dcr-1555ajk", "dcr-uo85ve"])
    )

    for s in soup:
        a_tags = s.find_all("a", class_=["dcr-2yd10d", "dcr-dqajlz"])
        for a_tag in a_tags:
            if a_tag and "href" in a_tag.attrs:
                article_url = f"https://www.theguardian.com{a_tag['href'].replace('https://www.theguardian.com', '')}"
                process_article(article_url)
