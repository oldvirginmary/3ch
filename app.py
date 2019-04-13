# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

import config


app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def index():
    from forms import ArticleForm
    from models import Article

    articles = Article.query.order_by(Article.time.desc()).all()
    return render_template('index.html', articles=articles)


@app.route('/article/<int:article_id>', methods=['POST', 'GET'])
def article(article_id):
    from forms import CommentForm
    from models import Comment

    if request.method == 'POST':
        form = CommentForm(request.form)

        if form.validate():
            comment = Comment(**form.data)
            db.session.add(comment)
            db.session.commit()

    this_article = Article.query.filter_by(id=article_id).first()
    comments = Comment.query.filter_by(article_id=this_article.id)
    return render_template('article.html', article=this_article, comments=comments)


@app.route('/new_article', methods=['GET', 'POST'])
def new_article():
    from forms import ArticleForm
    from models import Article

    if request.method == 'POST':
        form = ArticleForm(request.form)

        if form.validate():
            article = Article(**form.data)
            db.session.add(article)
            db.session.commit()

    return render_template('new_article.html')


if __name__ == '__main__':
    from models import *

    db.create_all()

    app.run()
