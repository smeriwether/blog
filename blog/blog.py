from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from datetime import datetime
import pytz

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


def format_datetime(value, include_relative=True):
    eastern = pytz.timezone('US/Eastern')
    if value.tzinfo is None:
        value = pytz.utc.localize(value)
    eastern_dt = value.astimezone(eastern)

    # Get current time in Eastern
    now = datetime.now(eastern)

    # Calculate time difference
    diff = now - eastern_dt

    if include_relative:
        if diff.days == 0:
            if diff.seconds < 60:
                return 'just now'
            if diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
            if diff.seconds < 86400:
                hours = diff.seconds // 3600
                return f'{hours} hour{"s" if hours != 1 else ""} ago'
        if diff.days == 1:
            return 'Yesterday'
        if diff.days < 7:
            return f'{diff.days} days ago'

    # Fall back to regular format for older dates
    return eastern_dt.strftime('%B %d, %Y %I:%M %p %Z')

bp.add_app_template_filter(nl2br, 'nl2br')
bp.add_app_template_filter(format_datetime, 'format_datetime')
