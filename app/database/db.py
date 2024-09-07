import numpy as np
from app import db
from app.models import Cluster, Article
from app.feature_engineering import clean_text, body_to_vectors
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta


def news_already_in_db(article_url):
    return Article.query.filter_by(url=article_url).first()


def get_clusters_from_db():
    clusters = [(cluster.id, list(map(float, cluster.cluster_center.split(',')))) for cluster in Cluster.query.all()]
    return clusters


def save_news_to_db(article_url, headline=None, formatted_date=None, body=None, sentiment=None, cluster=None):  # save url only for corpus
    try:
        article = Article(url=article_url, headline=headline, published_date=formatted_date, body=body, sentiment=sentiment, cluster=cluster)
        print(article)
        db.session.add(article)
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"Error saving article: {e}")
        db.session.rollback()
        return None
    finally:
        db.session.close()


def save_cluster_to_db(cluster_center, keywords):
    try:
        cluster_center = ','.join(map(str, cluster_center))
        cluster = Cluster(cluster_center=cluster_center, keywords=keywords)
        print(cluster)
        db.session.add(cluster)
        db.session.commit()
        return cluster
    except SQLAlchemyError as e:
        print(f"Error saving cluster: {e}")
        db.session.rollback()
        return None


def update_cluster_in_db(cluster_id, new_cluster_center, keywords):
    cluster = Cluster.query.get(cluster_id)
    cluster.cluster_center = ','.join(map(str, new_cluster_center))
    cluster.keywords = keywords
    db.session.commit()
    return cluster


def get_keywords(tfidf_matrix, feature_names):
    most_relevant_elements = np.argsort(-tfidf_matrix)[:5]
    keywords = ' '.join(feature_names[i] for i in most_relevant_elements)
    return keywords


def recalculate_cluster_center(cluster_id):
    cluster = Cluster.query.get(cluster_id)
    articles = Article.query.filter_by(cluster_id=cluster.id).all()
    documents = (clean_text(article.body) for article in articles)
    tfidf_matrix, feature_names = body_to_vectors(documents)
    new_cluster_center = np.mean(tfidf_matrix.toarray(), axis=0).flatten()
    cluster.cluster_center = ','.join(map(str, new_cluster_center))
    cluster.keywords = get_keywords(new_cluster_center, feature_names)
    print(f'cluster id: {cluster_id}\nrecalculate cluster center: {cluster.cluster_center}\nrecalculate keywords: {cluster.keywords}')


def delete_old_news():
    cutoff_date = datetime.now() - timedelta(days=1)

    articles_to_delete = Article.query.filter(Article.published_date < cutoff_date).all()
    affected_clusters = {article.cluster_id for article in articles_to_delete if article.cluster_id}

    Article.query.filter(Article.published_date < cutoff_date).delete()
    db.session.commit()

    for cluster_id in affected_clusters:
        cluster = Cluster.query.get(cluster_id)
        if len(cluster.articles) == 0:
            db.session.delete(cluster)
            print(f"Deleting orphaned cluster {cluster.id}")
        else:
            recalculate_cluster_center(cluster_id)
    db.session.commit()
