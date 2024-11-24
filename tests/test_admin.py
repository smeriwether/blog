from blog.db import get_db


def test_home(client):
    response = client.get("/admin")
    assert b"Adminland" in response.data


def test_home_lists_all_messages(client):
    response = client.get("/admin")
    assert b"happy content2" in response.data
    assert b"happy content1" in response.data


def test_home_can_create_a_new_message(client):
    response = client.get("/admin")
    assert b'href="/admin/message/new"' in response.data


def test_create_message_creates_a_new_message(client, app):
    client.post("/admin/message/create", data={"body": "this is a test"})
    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM message").fetchone()[0]
        assert count == 3


def test_create_message_validates_body(client, app):
    response = client.post("/admin/message/create", data={"body": ""})
    assert response.status_code == 400


def test_create_message_validates_body_has_content(client, app):
    response = client.post("/admin/message/create", data={"body": "  "})
    assert response.status_code == 400
