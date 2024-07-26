from web_scrapers import crawl_dailymail, crawl_guardian
from database import create_db


def main():
    create_db()
    crawl_dailymail()
    crawl_guardian()


if __name__ == '__main__':
    main()
