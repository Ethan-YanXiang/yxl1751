from web_scrapers import dailymail_scraper, guardian_scraper
from database import create_db


def main():
    create_db()
    dailymail_scraper()
    guardian_scraper()


if __name__ == '__main__':
    main()
