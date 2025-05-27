from .dailymail_scraper import dailymail_scraper
from .dailymirror_scraper import dailymirror_scraper
from .theguardian_scraper import theguardian_scraper
from .thesun_scraper import thesun_scraper


__all__ = ['run_all_scrapers']


def run_all_scrapers():

    dailymail_scraper()
    # dailymirror_scraper()
    # theguardian_scraper()
    # thesun_scraper()
