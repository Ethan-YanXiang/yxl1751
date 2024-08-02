from web_scrapers import dailymail_scraper, guardian_scraper
from database import create_db
from data_collection.feature_engineering import train_and_save_tfidf_vectorizer, body_to_vectors
from data_collection.unsupervised_machine_learning import real_time_single_pass_clustering


def main():
    create_db()
    dailymail_bodies = dailymail_scraper()
    guardian_bodies = guardian_scraper()

    if dailymail_bodies is None:
        dailymail_bodies = []
    if guardian_bodies is None:
        guardian_bodies = []

    all_bodies = dailymail_bodies + guardian_bodies
    if not all_bodies:
        print("No articles were scraped.")
        return

    tfidf_vectorizer = train_and_save_tfidf_vectorizer(all_bodies)
    for body in all_bodies:
        tfidf_matrix, feature_names = body_to_vectors(body, tfidf_vectorizer)
        real_time_single_pass_clustering(tfidf_matrix, feature_names)


if __name__ == '__main__':
    main()
