"""
REST API blueprint — CRUD for tasks.
"""

from flask import Blueprint, jsonify, request, abort
from .database import db
from .models import Task

api_bp = Blueprint("api", __name__)


@api_bp.get("/tasks")
def list_tasks():
    """Return all tasks."""
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks]), 200


@api_bp.post("/tasks")
def create_task():
    """Create a new task.

    Expects JSON body: ``{"title": "<string>"}``
    """
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    if not title:
        abort(400, description="'title' is required and must not be blank")

    task = Task(title=title)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@api_bp.get("/tasks/<int:task_id>")
def get_task(task_id):
    """Return a single task by ID."""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200


@api_bp.patch("/tasks/<int:task_id>")
def update_task(task_id):
    """Toggle or rename an existing task.

    Accepts optional JSON fields: ``title``, ``done``.
    """
    task = Task.query.get_or_404(task_id)
    data = request.get_json(silent=True) or {}

    if "title" in data:
        title = data["title"].strip()
        if not title:
            abort(400, description="'title' must not be blank")
        task.title = title

    if "done" in data:
        task.done = bool(data["done"])

    db.session.commit()
    return jsonify(task.to_dict()), 200


@api_bp.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    """Delete a task."""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return "", 204
