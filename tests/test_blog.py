import pytest
from blog.db import get_db

def test_index(client):
    response = client.get('/posts')
    assert b'test<br>body' in response.data

def test_create(client, app):
    client.post('/posts', data={'body': 'this is another test'})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2
        
def test_show(client, app):
    response = client.get('/posts/1')
    assert b'test\nbody' in response.data
