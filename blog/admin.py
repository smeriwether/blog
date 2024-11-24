from flask import Blueprint, abort, redirect, render_template, request, url_for

from blog.jinja_utils import relative_datetime
from blog.message_db import MessageDb

bp = Blueprint("admin", __name__)


@bp.route("/admin", methods=["GET"])
def home():
    message_db = MessageDb()
    messages = message_db.all()
    return render_template("admin/index.html", messages=messages)


@bp.route("/admin/message/new", methods=["GET"])
def new_message():
    return render_template("admin/new_message.html")


@bp.route("/admin/message/create", methods=["POST"])
def create_message():
    message_db = MessageDb()
    body = str(request.form["body"]).strip()
    if not body:
        abort(400)

    message_db.create(body)

    return redirect(url_for("admin.home"))


bp.add_app_template_filter(relative_datetime, "relative_datetime")
