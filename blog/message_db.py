from blog.db import get_db

class MessageDb:
    def __init__(self):
        self.db = get_db()


    def last(self):
        return self.db.execute(
            'SELECT * FROM message ORDER BY created_at DESC LIMIT 1'
        ).fetchone()
