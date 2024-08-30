from app import app, db
# 從 py檔(模組) 調用 實例
from app.forms import LoginForm, RegistrationForm
# 從 包.py檔(模組) 調用 類
from app.models import Article, Cluster

from flask import render_template, redirect, url_for, flash, request
# 從 包 調用 模組


@app.route('/')
@app.route('/index')
def home_func():
    sort_order = request.args.get('sort', 'desc')

    total_clusters = Cluster.query.count()
    total_articles = Article.query.count()

    subquery = db.session.query(Article.cluster_id, db.func.count(Article.id).label('count')).group_by(Article.cluster_id).subquery()
    hot_topics = db.session.query(subquery).filter(subquery.c.count >= 2).count()

    hot_topics_ids = db.session.query(Article.cluster_id).join(Cluster).group_by(Article.cluster_id).having(db.func.count(Article.id) >= 2).subquery()
    hot_news = db.session.query(Article).join(hot_topics_ids, Article.cluster_id == hot_topics_ids.c.cluster_id).count()

    if sort_order == 'desc':
        clusters_with_multiple_articles = Cluster.query \
            .join(Article) \
            .group_by(Cluster.id) \
            .having(db.func.count(Article.id) >= 2) \
            .order_by(db.func.count(Article.id).desc()) \
            .all()
    else:
        clusters_with_multiple_articles = Cluster.query \
            .join(Article) \
            .group_by(Cluster.id) \
            .having(db.func.count(Article.id) >= 2) \
            .order_by(db.func.count(Article.id).asc()) \
            .all()

    topics_with_news = []
    for topic in clusters_with_multiple_articles:
        news_list = Article.query.filter_by(cluster_id=topic.id).order_by(Article.published_date.desc()).all()

        earliest_news = min(news_list, key=lambda news: news.published_date)
        # summary = earliest_news.title
        topics_with_news.append({'topic': topic, 'news_list': news_list, 'news_count': len(news_list)})

    return render_template('index.html', total_clusters=total_clusters, total_articles=total_articles, hot_topics=hot_topics, hot_news=hot_news, topics_with_news=topics_with_news)


@app.route('/article/<int:article_id>')
def show_article(article_id):
    article = Article.query.get(article_id)
    return render_template('article.html', article=article, title=article.headline)


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
