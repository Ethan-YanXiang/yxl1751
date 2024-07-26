import os
import sqlite3

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '..', 'web_scrapers.sqlite')


def create_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        headline TEXT,
        published_date TEXT,
        body TEXT,
        url TEXT UNIQUE
    )
    ''')

    conn.commit()
    conn.close()


def save_news_to_db(article_data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO news (headline, published_date, body, url)
    VALUES (?, ?, ?, ?)
    ''', article_data)

    conn.commit()
    conn.close()


def news_already_in_db(article_url):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM news WHERE url=?', (article_url,))
    exists = cursor.fetchone() is not None

    conn.close()
    return exists


create_db()
