from web_scrapers import dailymail_scraper, guardian_scraper
from database import create_db


def main():
    from full_stack_development.app import app

    with app.app_context():
        create_db()

        dailymail_scraper() and guardian_scraper()


if __name__ == '__main__':
    main()
