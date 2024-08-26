import os
# 從 包 調用 模組
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = b'WR#&f&+%78er0we=%799eww+#7^90-;s'
# set up as soon as the app is initialised to prevent cross site scripting
basedir = os.path.abspath(os.path.dirname(__file__))  # using os to find the abspath of the running web app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'data.sqlite')
# creating our database file by joining the web app and prefix 'sqlite:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # preventing getting error message
db = SQLAlchemy(app)  # all the interactions to the database are gonna come through this variable


from app import routes
# from app package import views module
# putting all the routes inside our app
from app.models import *  # we need all the classes in app.models for the following steps


@app.shell_context_processor  # tell flask shell to import these variables to db.create_all(); db.session.commit()
def make_shell_context():
    return dict(db=db, Article=Article, Cluster=Cluster, datetime=datetime)
