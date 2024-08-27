from app import app
from app import db
from app.feature_engineering.tfidf_vectorizer import train_and_save_tfidf_vectorizer
from app.web_scrapers.dailymail_scraper import dailymail_scraper
from app.web_scrapers.guardian_scraper import guardian_scraper
from app.web_scrapers.dailymirror_scraper import dailymirror_scraper


def main():
    with app.app_context():
        db.create_all()
        train_and_save_tfidf_vectorizer()  # when corpus

        dailymail_scraper()
        guardian_scraper()
        dailymirror_scraper()


if __name__ == '__main__':
    main()
