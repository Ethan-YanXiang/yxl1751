from app import db
from app.models import Cluster, Article
from sqlalchemy.exc import SQLAlchemyError


def news_already_in_db(article_url):
    return Article.query.filter_by(url=article_url).first()


def get_clusters_from_db():
    clusters = [(cluster.id, list(map(float, cluster.cluster_center.split(',')))) for cluster in Cluster.query.all()]
    return clusters


def save_news_to_db(article_url, headline=None, published_date=None, body=None):  # save url only for corpus
    try:
        article = Article(headline=headline, published_date=published_date, body=body, url=article_url)
        print(article)
        db.session.add(article)
        db.session.commit()
        return article.id
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
        return cluster.id
    except SQLAlchemyError as e:
        print(f"Error saving cluster: {e}")
        db.session.rollback()
        return None
    finally:
        db.session.close()


def update_cluster_in_db(cluster_id, cluster_center, keywords):
    cluster = Cluster.query.get(cluster_id)
    cluster_center = ','.join(map(str, cluster_center))
    cluster.cluster_center = cluster_center
    cluster.keywords = keywords
    db.session.commit()


def link_cluster_in_db(article_id, cluster_id):
    article = Article.query.get(article_id)
    article.cluster_id = cluster_id
    db.session.commit()
