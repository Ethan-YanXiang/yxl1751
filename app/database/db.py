from app import db
from app.models import Cluster, Article


def news_already_in_db(article_url):
    return Article.query.filter_by(url=article_url).first() is not None


def save_news_to_db(url, headline=None, published_date=None, body=None):
    article = Article(headline=headline, published_date=published_date, body=body, url=url)
    db.session.add(article)
    db.session.commit()
    return article.id


def save_cluster_to_db(cluster_center, keywords):
    cluster = Cluster(cluster_center=cluster_center, keywords=keywords)
    db.session.add(cluster)
    db.session.commit()
    return cluster.id


def update_cluster_in_db(cluster_id, cluster_center, keywords):
    cluster = Cluster.query.get(cluster_id)
    cluster.cluster_center = cluster_center
    cluster.keywords = keywords
    db.session.commit()


def get_clusters_from_db():
    clusters = Cluster.query.all()
    return [(cluster.id, cluster.cluster_center, cluster.keywords.split(',')) for cluster in clusters]


def link_cluster_in_db(article_id, cluster_id):
    article = Article.query.get(article_id)
    article.cluster_id = cluster_id
    db.session.commit()
