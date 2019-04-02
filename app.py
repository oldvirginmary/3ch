# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

import config


app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    from forms import ArticleForm
    from models import Article

    if request.method == 'POST':
        print(request.form)
        form = ArticleForm(request.form)

        if form.validate():
            article = Article(**form.data)
            db.session.add(article)
            db.session.commit()

    articles = Article.query.all()
    return render_template('index.html', articles=articles)


@app.route('/article/<int:article_id>', methods=['POST', 'GET'])
def article(article_id):
    if request.method == 'POST':
        pass

    this_article = Article.query.filter_by(id=article_id).first()
    comments = Comment.query.filter_by(article_id=this_article.id)
    return render_template('article.html', article=this_article, comments=comments)


@app.route('/comments', methods=['POST', 'GET'])
def comments():
    from forms import CommentForm
    from models import Comment

    if request.method == 'POST':
        print(request.form)
        form = CommentForm(request.form)
        print(form.data, form.validate())

        if form.validate():
            comment = Comment(**form.data)
            db.session.add(comment)
            db.session.commit()

    all_articles = Article.query.all()
    all_comments = Comment.query.all()

    # article_comments = [] # two-dimensional array
    # for article in all_articles:
    #     comments = Comment.query.filter(article.id == Comment.article_id).all()
    #     article_comments.append(comments)

    # print(all_articles)
    # print(article_comments)

    return render_template('index.html', articles=all_articles, comments=all_comments)


if __name__ == '__main__':
    from models import *

    db.create_all()

    app.run()
