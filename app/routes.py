from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import Article, Cluster
from app.llama3.Ollama import llama3_summary, llama3_sentiment
from flask import render_template, redirect, url_for, flash, request


@app.route('/')
@app.route('/index')
def home_func():
    sort_order = request.args.get('sort', 'desc')

    total_clusters = Cluster.query.count()
    total_articles = Article.query.count()

    subquery = db.session.query(Article.cluster_id, db.func.count(Article.id).label('count')).group_by(Article.cluster_id).subquery()
    total_hot_topics = db.session.query(subquery).filter(subquery.c.count >= 2).count()

    hot_topics_ids = db.session.query(Article.cluster_id).join(Cluster).group_by(Article.cluster_id).having(db.func.count(Article.id) >= 2).subquery()
    total_hot_news = db.session.query(Article).join(hot_topics_ids, Article.cluster_id == hot_topics_ids.c.cluster_id).count()

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
    for hot_topic in clusters_with_multiple_articles:
        hot_news_list = Article.query.filter_by(cluster_id=hot_topic.id).order_by(Article.published_date.desc()).all()

        topics_with_news.append({'hot_topic': hot_topic, 'hot_news_list': hot_news_list, 'news_count': len(hot_news_list)})

    return render_template('index.html', total_clusters=total_clusters, total_articles=total_articles, total_hot_topics=total_hot_topics, total_hot_news=total_hot_news, topics_with_news=topics_with_news)


@app.route('/article/<int:article_id>')
def show_article(article_id):
    article = Article.query.get(article_id)
    summary = llama3_summary(article.url)
    # sentiment = llama3_sentiment(article.url)
    return render_template('article.html', article=article, summary=summary, title=article.headline)


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
