# -*- coding: utf-8 -*-
from flask import render_template, Flask, request, redirect, url_for, flash, g, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from app import app, db
from app.models import Article, Comment, UserInfo
from app.forms import ArticleForm, CommentForm, JoinForm, LoginForm


@app.before_request
def before_request():
    g.user_name = None

    if 'user_id' in session:
        g.user_name = session['user_name']


@app.route('/', methods=['GET'])
def article_list():
    context = {}

    context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()

    return render_template('home.html', context=context, active_tab='timeline')


@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    if g.user_name is None:
        flash(u'로그인 후에 이용해 주세요', 'danger')
        return redirect(url_for('login'))
    else:
        form = ArticleForm()

        if request.method == 'POST':
            if form.validate_on_submit():

                article = Article(
                    title=form.title.data,
                    author=form.author.data,
                    category=form.category.data,
                    content=form.content.data
                )

                db.session.add(article)
                db.session.commit()

                flash(u'게시글 작성하였습니다.', 'success')
                return redirect(url_for('article_list'))
        return render_template('article/create.html', form=form, active_tab='article_create')


@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
    article = Article.query.get(id)

    comments = article.comments.order_by(desc(Comment.date_created)).all()
    return render_template('article/detail.html', article=article, comments=comments)


@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    article = Article.query.get(id)
    form = ArticleForm(request.form, obj=article)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(article)
            db.session.commit()
        return redirect(url_for('article_detail', id=id))

    return render_template('article/update.html', form=form)


@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
    if request.method == 'POST':
        article_id = request.form.get('article_id')
        article = Article.query.get(article_id)
        db.session.delete(article)
        db.session.commit()

        flash(u'게시글을 삭제하였습니다.', 'success')
        return redirect(url_for('article_list'))
    return render_template('article/delete.html', article_id=id)


#
# @comment controllers
#
@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
    form = CommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = Comment(
                author=form.author.data,
                email=form.email.data,
                content=form.content.data,
                password=form.password.data,
                article=Article.query.get(article_id),
                like=0
            )

            db.session.add(comment)
            db.session.commit()

            flash(u'댓글을 작성하였습니다.', 'success')
            return redirect(url_for('article_detail', id=article_id))
    return render_template('comment/create.html', form=form)


@app.route('/comment/like/<int:id>', methods=['GET'])
def comment_like(id):
    comment = Comment.query.get(id)

    comment.like += 1
    db.session.commit()

    return redirect(url_for('article_detail', id=comment.article_id))


@app.route('/comment/delete/<int:id>', methods=['GET', 'POST'])
def comment_delete(id):
    if request.method == 'POST':
        password = request.form.get('password')
        comment = Comment.query.get(id)

        if comment.password == password:
            db.session.delete(comment)
            db.session.commit()
            flash(u'댓글을 삭제하였습니다.', 'success')

        return redirect(url_for('article_detail', id=comment.article_id))
    return render_template('comment/delete.html')


@app.route('/login/register/', methods=['GET', 'POST'])
def register():
    form = JoinForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            if db.session.query(UserInfo).filter(UserInfo.email == form.email.data).count() > 0:
                flash(u'이미 가입한 이메일입니다.', 'danger')
                return render_template('login/register.html', form=form, active_tab=register)
            else:
                new_user = UserInfo(
                    email=form.email.data,
                    password=generate_password_hash(form.password.data),
                    name=form.name.data,
                )

                db.session.add(new_user)
                db.session.commit()

                flash(u'회원가입 성공했습니다.', 'success')
                return redirect(url_for('article_list'))
    return render_template('login/register.html', form=form, active_tab='register')


@app.route('/login/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.query(UserInfo).filter(UserInfo.email == form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                # login success
                session['user_id'] = user.id
                session['user_name'] = user.name

                return redirect(url_for('article_list'))
            else:
                return render_template('login/login.html', form=form, active_tab='login')
    return render_template('login/login.html', form=form, active_tab='login')


@app.route('/login/logout/')
def logout():
    session.clear()
    return redirect(url_for('article_list'))


#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
