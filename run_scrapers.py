from app import app, db
from app.feature_engineering.tfidf_vectorizer import train_and_save_tfidf_vectorizer
from app.web_scrapers.dailymail_scraper import dailymail_scraper
from app.web_scrapers.theguardian_scraper import theguardian_scraper
from app.web_scrapers.dailymirror_scraper import dailymirror_scraper
from app.web_scrapers.thesun_scraper import thesun_scraper


def main():
    with app.app_context():
        db.create_all()
        train_and_save_tfidf_vectorizer()  # when corpus

        dailymail_scraper()
        dailymirror_scraper()
        theguardian_scraper()
        thesun_scraper()


if __name__ == '__main__':
    main()
