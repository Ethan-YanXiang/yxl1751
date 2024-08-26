from app import db


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    headline = db.Column(db.String, nullable=False)  # True
    published_date = db.Column(db.String, nullable=False)  # True
    body = db.Column(db.Text, nullable=False)  # True
    url = db.Column(db.String, nullable=False, unique=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'))

    def __repr__(self):
        return f"article('{self.headline}', '{self.published_date}', '{self.body}' , '{self.url}')"


class Cluster(db.Model):
    __tablename__ = 'clusters'
    id = db.Column(db.Integer, primary_key=True)
    cluster_center = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String, nullable=False)
    articles = db.relationship('Article', backref='cluster', lazy=True)

    def __repr__(self):
        return f"cluster('{self.cluster_center}', '{self.keywords}')"
