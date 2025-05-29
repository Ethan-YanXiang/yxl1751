from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import Article, Cluster, User
from app.large_language_model.Ollama import llama3_summary
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit


@app.route("/")
@app.route("/index")
@login_required
def home_func():
    sort_order = request.args.get("sort", "desc")

    total_clusters = Cluster.query.count()
    total_articles = Article.query.count()

    subquery = (
        db.session.query(Article.cluster_id, db.func.count(Article.id).label("count"))
        .group_by(Article.cluster_id)
        .subquery()
    )
    total_hot_topics = db.session.query(subquery).filter(subquery.c.count >= 3).count()

    hot_topics_ids = (
        db.session.query(Article.cluster_id)
        .join(Cluster)
        .group_by(Article.cluster_id)
        .having(db.func.count(Article.id) >= 3)
        .subquery()
    )
    total_hot_news = (
        db.session.query(Article)
        .join(hot_topics_ids, Article.cluster_id == hot_topics_ids.c.cluster_id)
        .count()
    )

    if sort_order == "desc":
        clusters_with_multiple_articles = (
            Cluster.query.join(Article)
            .group_by(Cluster.id)
            .having(db.func.count(Article.id) >= 3)
            .order_by(db.func.count(Article.id).desc())
            .all()
        )
    else:
        clusters_with_multiple_articles = (
            Cluster.query.join(Article)
            .group_by(Cluster.id)
            .having(db.func.count(Article.id) >= 3)
            .order_by(db.func.count(Article.id).asc())
            .all()
        )

    topics_with_news = []
    for hot_topic in clusters_with_multiple_articles:
        hot_news_list = (
            Article.query.filter_by(cluster_id=hot_topic.id)
            .order_by(Article.published_date.desc())
            .all()
        )

        topics_with_news.append(
            {
                "hot_topic": hot_topic,
                "hot_news_list": hot_news_list,
                "news_count": len(hot_news_list),
            }
        )

    return render_template(
        "index.html",
        total_clusters=total_clusters,
        total_articles=total_articles,
        total_hot_topics=total_hot_topics,
        total_hot_news=total_hot_news,
        topics_with_news=topics_with_news,
    )


@app.route("/article/<int:article_id>")
@login_required
def article_func(article_id):
    article = Article.query.get(article_id)
    summary = llama3_summary(article.url)
    return render_template(
        "article.html", article=article, summary=summary, title=article.headline
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home_func"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "danger")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        flash(f"Login for {form.username.data}", "success")
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("home_func")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout_func():
    logout_user()
    return redirect(url_for("home_func"))


@app.route("/register", methods=["GET", "POST"])
def register_func():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_exists = User.query.filter_by(username=form.username.data).first()
        email_exists = User.query.filter_by(email=form.email.data).first()
        if user_exists:
            flash("Username already exists.")
            return render_template("registration.html", title="Register", form=form)
        if email_exists:
            flash(" Email already exists.")
            return render_template("registration.html", title="Register", form=form)

        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash(f"Registration for {form.username.data} received", "success")
        return redirect(url_for("home_func"))
    return render_template("registration.html", title="Register", form=form)
