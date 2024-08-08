from database import create_db
from feature_engineering import train_and_save_tfidf_vectorizer
from web_scrapers import dailymail_scraper, guardian_scraper


def main():
    from full_stack_development.app import app

    with app.app_context():
        create_db()

        train_and_save_tfidf_vectorizer()

        dailymail_scraper()
        guardian_scraper()


if __name__ == '__main__':
    main()
