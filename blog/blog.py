from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from blog.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/posts', methods=['GET', 'POST'])
def posts():
    db = get_db()
    if request.method == 'POST':
        body = request.form['body']
        if not body:
            abort(400)
        
        db.execute(
            'INSERT INTO post (body) VALUES (?)',
            (body,),
        )
        db.commit()
        return redirect(url_for('blog.posts'))
    else:
        posts = db.execute(
            'SELECT * FROM post ORDER BY created DESC'
        ).fetchall()
        message = db.execute(
            'SELECT * FROM message ORDER BY created DESC'
        ).fetchone()
        return render_template('posts/index.html', posts=posts, message=message)

# SHOW - GET /posts/<id>
@bp.route('/posts/<int:post_id>', methods=['GET'])
def show_post(post_id):
    db = get_db()
    post = db.execute(
        'SELECT * FROM post WHERE id = ?',
        (post_id,),
    ).fetchone()
    return render_template('posts/show.html', post=post)

# Root redirect
@bp.route('/')
def index():
    return redirect(url_for('blog.posts'))


def nl2br(value):
    if not value:
        return value
    return value.replace('\n', '<br>')

bp.add_app_template_filter(nl2br, 'nl2br')
