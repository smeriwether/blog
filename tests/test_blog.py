from blog.db import get_db


def test_index(client):
    response = client.get("/posts")
    assert b"test\nbody" in response.data


def test_index_does_not_return_deleted_posts(client):
    response = client.get("/posts")
    assert b"test deleted" not in response.data


def test_index_includes_most_recent_message(client):
    response = client.get("/posts")
    assert b"happy content2" in response.data


def test_index_show_favorite_icon(client, app):
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET favorite = 1 WHERE id = 1")
        db.commit()

    response = client.get("/posts")
    assert b"Favorite" in response.data


def test_create(client, app):
    client.post("/posts", data={"body": "this is another test"})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM post").fetchone()[0]
        assert count == 3


def test_create_validates_body(client):
    response = client.post("/posts", data={"body": ""})
    assert response.status_code == 400


def test_create_validates_body_has_content(client):
    response = client.post("/posts", data={"body": "    "})
    assert response.status_code == 400


def test_show(client):
    response = client.get("/posts/1")
    assert b"test\nbody" in response.data


def test_show_does_not_show_deleted_posts(client):
    response = client.get("/posts/2")
    assert response.status_code == 404


def test_show_can_favorite_posts(client):
    response = client.get("/posts/1")
    assert b"Favorite" in response.data


def test_show_can_unfavorite_posts_that_are_favorited(client, app):
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET favorite = 1 WHERE id = 1")
        db.commit()

    response = client.get("/posts/1")
    assert b"Favorite" not in response.data
    assert b"Unfavorite" in response.data


def test_edit(client, app):
    response = client.get("/posts/1/edit")
    assert response.status_code == 200
    assert b"test\nbody" in response.data
    assert b"Update" in response.data


def test_edit_validate_post_exists(client, app):
    # Test with non-existent post
    response = client.get("/posts/99999/edit")
    assert response.status_code == 404


def test_edit_validate_not_deleted(client, app):
    # Using id of deleted post
    response = client.get("/posts/2/edit")
    assert response.status_code == 404


def test_update(client, app):
    client.post("/posts/1/update", data={"body": "test<br>body 1"})
    with app.app_context():
        db = get_db()
        result = db.execute("SELECT body, updated_at, created_at FROM post").fetchone()
        assert "test<br>body 1" in result[0]
        assert result[1] > result[2]


def test_update_validates_post_exists(client, app):
    response = client.post("/posts/9999/update")
    assert response.status_code == 404


def test_update_validates_body(client, app):
    response = client.post("/posts/1/update", data={"body": ""})
    assert response.status_code == 400


def test_update_validates_body_has_content(client, app):
    response = client.post("/posts/1/update", data={"body": "    "})
    assert response.status_code == 400


def test_delete(client, app):
    client.post("/posts/1/delete")
    with app.app_context():
        db = get_db()
        count = db.execute(
            "SELECT COUNT(id) FROM post WHERE deleted_at = NULL"
        ).fetchone()[0]
        assert count == 0


def test_delete_validates_post_exists(client, app):
    response = client.post("/posts/9999/delete")
    assert response.status_code == 404


def test_favorite_marks_post_as_favorite(client, app):
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET favorite = 0 WHERE id = 1")
        db.commit()

    client.post("/posts/1/favorite")

    with app.app_context():
        db = get_db()
        response = db.execute("SELECT favorite FROM post WHERE id = 1").fetchone()[0]
        assert response == 1


def test_favorite_validates_post_exists(client):
    response = client.post("/posts/9999/favorite")
    assert response.status_code == 404


def test_unfavorite_marks_post_as_unfavorite(client, app):
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET favorite = 1 WHERE id = 1")
        db.commit()

    response = client.post("/posts/1/unfavorite")

    with app.app_context():
        db = get_db()
        response = db.execute("SELECT favorite FROM post WHERE id = 1").fetchone()[0]
        assert response == 0


def test_unfavorite_validates_post_exists(client):
    response = client.post("/posts/9999/unfavorite")
    assert response.status_code == 404
