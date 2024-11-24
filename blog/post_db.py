from datetime import datetime

from blog.db import get_db


class PostDb:
    def __init__(self):
        self.db = get_db()

    def all(self):
        return self.db.execute(
            "SELECT * FROM post WHERE deleted_at IS NULL ORDER BY created_at DESC"
        ).fetchall()

    def find(self, post_id):
        return self.db.execute(
            "SELECT * FROM post WHERE id = ? AND deleted_at IS NULL", (post_id,)
        ).fetchone()

    def create(self, post_body):
        self.db.execute(
            "INSERT INTO post (body) VALUES (?) ",
            (post_body,),
        )
        self.db.commit()

    def update(self, post_id, post_body):
        self.db.execute(
            "UPDATE post SET body = ?, updated_at = ? WHERE id = ?",
            (post_body, datetime.now(), post_id),
        )
        self.db.commit()

    def delete(self, post_id):
        self.db.execute(
            "UPDATE post SET deleted_at = ? WHERE id = ?",
            (datetime.now(), post_id),
        )
        self.db.commit()

    def favorite(self, post_id):
        self.db.execute(
            "UPDATE post SET favorite = 1, updated_at = ? WHERE id = ?",
            (datetime.now(), post_id),
        )
        self.db.commit()

    def unfavorite(self, post_id):
        self.db.execute(
            "UPDATE post SET favorite = 0, updated_at = ? WHERE id = ?",
            (datetime.now(), post_id),
        )
        self.db.commit()
