from flask import render_template, flash, redirect, request, url_for, g
from app.forms import PostForm, UserSearchForm
from flask_login import current_user, login_required
from app.models import Post, User
from . import bp as social
from app import app


@app.before_request
def before_request():
    g.search_form = UserSearchForm()
    g.post_form = PostForm()


@social.post('/post')
@login_required
def post():
    post = Post(body=g.post_form.body.data, user_id=current_user.user_id)
    post.commit()
    flash('Posted', category='success')
    return redirect(url_for('social.profile', username=current_user.username))

@social.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        posts = user.posts
        return render_template('profile.jinja', username=username, posts=posts)
    else:
        flash(f'User: {username} not found', category='warning')
        return redirect(url_for('main.home', search_form=g.search_form))


@social.post('/user-search')
def user_search():
    return redirect(url_for('social.profile', username=g.search_form.username.data))