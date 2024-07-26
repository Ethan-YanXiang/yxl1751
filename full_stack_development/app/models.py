from app import db
# from package app import db: SQLAlchemy(app)


class News(db.Model):  # models classes inherit from 'db.Model'
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)  # if primary_key=True, then (unique=True, nullable=False)
    headline = db.Column(db.Text, nullable=False)  # and SQLAlchemy just make it autoIncremnet if (db.Integer, primary_key=True)
    published_date = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"news('{self.headline}', '{self.published_date}', '{self.body}' , '{self.url}')"
        # for an object, __repr__ generates the string representation the way we want in Flask server log
