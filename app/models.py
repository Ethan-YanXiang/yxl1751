from app import db


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, index=True)
    headline = db.Column(db.String, nullable=False)  # True when corpus
    published_date = db.Column(db.String, nullable=False)  # True when corpus
    body = db.Column(db.Text, nullable=False)  # True when corpus
    url = db.Column(db.String, unique=True,  nullable=False, index=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'), nullable=True, index=True)
    # cluster_id corresponds to articles attrs, for each body can have one and only "one" cluster_id

    def __repr__(self):
        return f"article('{self.headline}', '{self.published_date}', '{self.body}' , '{self.url}', '{self.cluster}')"
        # '{self.cluster}': provides access to corresponding info in Cluster


class Cluster(db.Model):
    __tablename__ = 'clusters'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, index=True)
    cluster_center = db.Column(db.Text, nullable=False, index=True)
    keywords = db.Column(db.String, nullable=False)
    articles = db.relationship('Article', backref='cluster', lazy=True)  # virtual field
    # represent relationship to Article, for each cluster_center can have "many" articles
    # backref='cluster': putting a virtual field 'cluster' in Article for Article to reference corresponding cluster

    def __repr__(self):
        return f"cluster('{self.cluster_center}', '{self.keywords}', '{self.articles}')"
