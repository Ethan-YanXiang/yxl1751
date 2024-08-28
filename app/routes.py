from app import app, db
# 從 py檔(模組) 調用 實例
from app.forms import LoginForm, RegistrationForm
# 從 包.py檔(模組) 調用 類
from app.models import Article, Cluster

from flask import render_template, redirect, url_for, flash  # 一次性 error message
from datetime import datetime
# 從 包 調用 模組


@app.route('/')
@app.route('/index')
def home_func():
    return render_template('index.html')


@app.route('/datetime')
def time_func():
    now = datetime.now()
    return render_template('datetime.html', title='Date & Time', now=now)


@app.route('/login', methods=['GET', 'POST'])  # POST: safely send sensitive data to a server page
def login_func():
    form = LoginForm()  # 呼叫 LoginForm() 類，初始化一個 form object

    userdata = form.username.data
    password_data = form.password.data
    try:
        if userdata.lower() == 'admin':
            flash(f'Username can\'t be {form.username.data}', 'danger')
        elif not userdata.isalpha() and userdata:
            flash(f'Username must be alphanumeric', 'danger')
        elif not password_data.isdigit() and password_data:
            flash(f'Password must be digit', 'danger')
        elif len(password_data) < 4:
            flash(f'Password must be at least 4 characters', 'danger')
        elif form.validate_on_submit():  # all fields validate correctly, request via POST, return True.
            flash(f'Login for {form.username.data}', 'success')  # .data = data typed in
            return redirect(url_for('home_func'))  # once login, where should it go (POST)
    except AttributeError:
        pass

    return render_template('login.html', title='Sign In', form=form)
    # fetching the page first time (GET)


@app.route('/register', methods=['GET', 'POST'])
def register_func():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Registration for {form.username.data} received', 'success')
        return redirect(url_for('home_func'))
    return render_template('registration.html', title='Register', form=form)


@app.route('/clusters')
def show_clusters():
    clusters = Cluster.query.all()
    return render_template('clusters.html', clusters=clusters, title="News Clusters")


@app.route('/cluster/<int:cluster_id>')
def show_cluster_articles(cluster_id):
    cluster = Cluster.query.get_or_404(cluster_id)
    articles = Article.query.filter_by(cluster_id=cluster_id).all()
    return render_template('cluster_articles.html', cluster=cluster, articles=articles, title="Cluster Articles")


@app.route('/article/<int:article_id>')
def show_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article.html', article=article, title=article.headline)
