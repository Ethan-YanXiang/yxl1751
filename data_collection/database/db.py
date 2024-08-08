import os
from full_stack_development.app import db
from full_stack_development.app.models import Cluster, Article


def create_db():
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # if os.path.exists(basedir, 'data', 'data.sqlite'):
    #     with open(basedir, 'data', 'data.sqlite') as f:
    # else:
    db.create_all()


def news_already_in_db(article_url):
    return Article.query.filter_by(url=article_url).first() is not None


def save_news_to_db(headline, formatted_date, body, url, cluster_id=None):
    article = Article(headline=headline, published_date=formatted_date, body=body, url=url, cluster_id=cluster_id)
    db.session.add(article)
    db.session.commit()
    return article.id


def save_cluster_to_db(cluster_center, keywords):
    cluster = Cluster(cluster_center=cluster_center, keywords=','.join(keywords))
    db.session.add(cluster)
    db.session.commit()
    return cluster.id


def update_cluster_in_db(cluster_id, cluster_center, keywords):
    cluster = Cluster.query.get(cluster_id)
    cluster.cluster_center = cluster_center
    cluster.keywords = ','.join(keywords)
    db.session.commit()


def get_clusters_from_db():
    clusters = Cluster.query.all()
    return [(cluster.id, cluster.cluster_center, cluster.keywords.split(',')) for cluster in clusters]


def link_cluster_with_news(article_id, cluster_id):
    article = Article.query.get(article_id)
    article.cluster_id = cluster_id
    db.session.commit()
