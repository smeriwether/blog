from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from blog.post_db import PostDb
from blog.message_db import MessageDb
from blog.jinja_utils import relative_datetime, safe_html
from blog.utils import sanitize_html

bp = Blueprint('blog', __name__)


@bp.route('/posts', methods=['GET'])
def posts():
    post_db = PostDb()
    message_db = MessageDb()
    posts = post_db.all()
    message = message_db.last()
    return render_template('posts/index.html', posts=posts, message=message)

@bp.route('/posts', methods=['POST'])
def create_post():
    post_db = PostDb()
    body = sanitize_html(str(request.form['body']).strip())
    if not body:
        abort(400)

    post_db.create(body)

    return redirect(url_for('blog.posts'))

@bp.route('/posts/<int:post_id>', methods=['GET'])
def show_post(post_id):
    post_db = PostDb()
    post = post_db.find(post_id)

    if not post:
        abort(404)

    return render_template('posts/show.html', post=post)


@bp.route('/posts/<int:post_id>/edit', methods=['GET'])
def edit_post(post_id):
    post_db = PostDb()
    post = post_db.find(post_id)

    if not post:
        abort(404)

    return render_template('posts/edit.html', post=post)


@bp.route('/posts/<int:post_id>/update', methods=['POST'])
def update_post(post_id):
    post_db = PostDb()
    post = post_db.find(post_id)

    if not post:
        abort(404)

    body = sanitize_html(str(request.form['body']).strip())
    if not body:
        abort(400)

    post_db.update(post_id, body)

    return redirect(url_for('blog.show_post', post_id=post_id))


@bp.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post_db = PostDb()
    post = post_db.find(post_id)

    if not post:
        abort(404)

    post_db.delete(post_id)
    return redirect(url_for('blog.posts'))

@bp.route('/posts/<int:post_id>/favorite', methods=['POST'])
def favorite_post(post_id):
    post_db = PostDb()
    post = post_db.find(post_id)

    if not post:
        abort(404)

    post_db.favorite(post_id)
    return redirect(url_for('blog.show_post', post_id=post_id))

@bp.route('/posts/<int:post_id>/unfavorite', methods=['POST'])
def unfavorite_post(post_id):
    post_db = PostDb()
    post = post_db.find(post_id)

    if not post:
        abort(404)

    post_db.unfavorite(post_id)
    return redirect(url_for('blog.show_post', post_id=post_id))

@bp.route('/')
def index():
    return redirect(url_for('blog.posts'))

bp.add_app_template_filter(safe_html, 'safe_html')
bp.add_app_template_filter(relative_datetime, 'relative_datetime')
