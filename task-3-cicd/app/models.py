"""
SQLAlchemy models.
"""

from datetime import datetime, timezone
from .database import db


class Task(db.Model):
    """A simple task / to-do item stored in PostgreSQL."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self):
        """Serialize the model to a plain dict for JSON responses."""
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "created_at": self.created_at.isoformat(),
        }
