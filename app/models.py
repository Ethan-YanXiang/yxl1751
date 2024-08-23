from app import db


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    headline = db.Column(db.String)  # nullable=False
    published_date = db.Column(db.String)  # nullable=False
    body = db.Column(db.Text)  # nullable=False
    url = db.Column(db.String, unique=True, nullable=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'))

    def __repr__(self):
        return f"article('{self.headline}', '{self.published_date}', '{self.body}' , '{self.url}')"


class Cluster(db.Model):
    __tablename__ = 'clusters'
    id = db.Column(db.Integer, primary_key=True)
    cluster_center = db.Column(db.PickleType, nullable=False)  # Text
    keywords = db.Column(db.String, nullable=False)
    articles = db.relationship('Article', backref='cluster', lazy=True)

    def __repr__(self):
        return f"cluster('{self.cluster_center}', '{self.keywords}')"
