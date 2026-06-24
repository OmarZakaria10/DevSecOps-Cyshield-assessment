"""
Integration tests for the /api/tasks CRUD endpoints.

These tests exercise all four HTTP verbs and the most important
error paths.  In CI they run against a real PostgreSQL service
container; locally they fall back to SQLite (see conftest.py).
"""

import json


# ---------------------------------------------------------------------------
# LIST
# ---------------------------------------------------------------------------


def test_list_tasks_empty(client):
    """An empty database returns an empty JSON array."""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


# ---------------------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------------------


def test_create_task_success(client):
    """A valid POST creates a task and returns 201 with the new record."""
    response = client.post(
        "/api/tasks",
        data=json.dumps({"title": "Buy groceries"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body["title"] == "Buy groceries"
    assert body["done"] is False
    assert "id" in body
    assert "created_at" in body


def test_create_task_missing_title(client):
    """A POST without a title must be rejected with 400."""
    response = client.post(
        "/api/tasks",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_create_task_blank_title(client):
    """A POST with a whitespace-only title must be rejected with 400."""
    response = client.post(
        "/api/tasks",
        data=json.dumps({"title": "   "}),
        content_type="application/json",
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# READ
# ---------------------------------------------------------------------------


def test_get_task_success(client):
    """A GET for an existing ID returns 200 and the correct task."""
    create_resp = client.post(
        "/api/tasks",
        data=json.dumps({"title": "Read a book"}),
        content_type="application/json",
    )
    task_id = create_resp.get_json()["id"]

    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Read a book"


def test_get_task_not_found(client):
    """A GET for a non-existent ID returns 404."""
    response = client.get("/api/tasks/99999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------------------


def test_update_task_title(client):
    """A PATCH can rename a task."""
    task_id = client.post(
        "/api/tasks",
        data=json.dumps({"title": "Old title"}),
        content_type="application/json",
    ).get_json()["id"]

    response = client.patch(
        f"/api/tasks/{task_id}",
        data=json.dumps({"title": "New title"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.get_json()["title"] == "New title"


def test_update_task_done(client):
    """A PATCH can mark a task as done."""
    task_id = client.post(
        "/api/tasks",
        data=json.dumps({"title": "Exercise"}),
        content_type="application/json",
    ).get_json()["id"]

    response = client.patch(
        f"/api/tasks/{task_id}",
        data=json.dumps({"done": True}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.get_json()["done"] is True


def test_update_task_not_found(client):
    """A PATCH for a non-existent task returns 404."""
    response = client.patch(
        "/api/tasks/99999",
        data=json.dumps({"done": True}),
        content_type="application/json",
    )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------


def test_delete_task_success(client):
    """A DELETE removes the task and returns 204."""
    task_id = client.post(
        "/api/tasks",
        data=json.dumps({"title": "Temporary"}),
        content_type="application/json",
    ).get_json()["id"]

    del_resp = client.delete(f"/api/tasks/{task_id}")
    assert del_resp.status_code == 204

    # Verify it's gone
    get_resp = client.get(f"/api/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_delete_task_not_found(client):
    """A DELETE for a non-existent task returns 404."""
    response = client.delete("/api/tasks/99999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# LIST after creates
# ---------------------------------------------------------------------------


def test_list_tasks_after_creates(client):
    """List returns all created tasks."""
    titles = ["Alpha", "Beta", "Gamma"]
    for t in titles:
        client.post(
            "/api/tasks",
            data=json.dumps({"title": t}),
            content_type="application/json",
        )

    response = client.get("/api/tasks")
    assert response.status_code == 200
    returned_titles = [item["title"] for item in response.get_json()]
    assert set(returned_titles) == set(titles)
