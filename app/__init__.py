import os
# 從 包 調用 模組
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = b'WR#&f&+%78er0we=%799eww+#7^90-;s'  # set up to prevent cross site scripting
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # preventing getting error message
db = SQLAlchemy(app)  # all the interactions to the database come through this variable


from app import routes
# from app package import views module
# putting all the routes inside our app
from app.models import *


@app.shell_context_processor  # tell flask shell to import these variables to db.create_all(); db.session.commit()
def make_shell_context():
    return dict(db=db, Article=Article, Cluster=Cluster, datetime=datetime)
