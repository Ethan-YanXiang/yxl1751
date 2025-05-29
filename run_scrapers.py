import time

import schedule

from app import app, db
from app.database.db import delete_old_news
from app.feature_engineering import train_and_save_tfidf_vectorizer
from app.web_scrapers import run_all_scrapers


def main():
    with app.app_context():
        db.create_all()
        train_and_save_tfidf_vectorizer()  # when corpus

        delete_old_news()
        run_all_scrapers()


if __name__ == "__main__":
    main()

    schedule.every(30).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
