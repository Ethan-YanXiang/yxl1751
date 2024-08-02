from web_scrapers import dailymail_scraper, guardian_scraper
from database import create_db, save_news_to_db
from data_collection.feature_engineering import train_and_save_tfidf_vectorizer, body_to_vectors
from data_collection.unsupervised_machine_learning import real_time_single_pass_clustering
from full_stack_development.app import app


def main():
    with app.app_context():
        create_db()
        app_context = app.app_context()
        app_context.push()

        dailymail_bodies = dailymail_scraper(app_context)
        guardian_bodies = guardian_scraper(app_context)

        if dailymail_bodies is None:
            dailymail_bodies = []
        if guardian_bodies is None:
            guardian_bodies = []

        all_bodies = dailymail_bodies + guardian_bodies
        if not all_bodies:
            print("No articles were scraped.")
            return

        tfidf_vectorizer = train_and_save_tfidf_vectorizer([body['body'] for body in all_bodies])
        for body in all_bodies:
            tfidf_matrix, feature_names = body_to_vectors(body['body'], tfidf_vectorizer)
            cluster_id = real_time_single_pass_clustering(tfidf_matrix, feature_names)
            save_news_to_db(body['headline'], body['published_date'], body['body'], body['url'], cluster_id)


if __name__ == '__main__':
    main()
