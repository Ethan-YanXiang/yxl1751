from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, index=True)
    headline = db.Column(db.String, nullable=False)  # True when corpus
    published_date = db.Column(db.String, nullable=False)  # True when corpus
    body = db.Column(db.Text, nullable=False)  # True when corpus
    url = db.Column(db.String, unique=True,  nullable=False, index=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'), nullable=True, index=True)
    sentiment = db.Column(db.String(10))
    # cluster_id corresponds to articles attrs, for each body can have one and only "one" cluster_id

    def __repr__(self):
        return f"article('{self.headline}'\n'{self.published_date}'\n'{self.url}'\n'{self.sentiment}')"
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
        return f"cluster('{self.keywords}')"


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=32)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Since we named our primary key "user_id", instead of "id", we have to override the
    # get_id() from the UserMixin to return the id, and it has to be returned as a string
    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f"user(id='{self.user_id}', '{self.username}', '{self.email}')"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
