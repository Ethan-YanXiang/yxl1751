# 從 包 調用 模組
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = b'WR#&f&+%78er0we=%799eww+#7^90-;s'
# set up as soon as the app is initialised to prevent cross site scripting

from app import routes3
# from app package import views module
# putting all the routes inside our app
