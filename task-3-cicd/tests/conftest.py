"""
Shared pytest fixtures.

The DATABASE_URL environment variable is set by GitLab CI via the
`services:` block (PostgreSQL container). When running locally without
a real DB, the tests fall back to an in-memory SQLite database so
developers don't need Docker just to run the test suite quickly.
"""

import os
import pytest

from app import create_app
from app.database import db as _db


@pytest.fixture(scope="session")
def app():
    """Create the Flask app wired to the test database."""
    db_url = os.getenv(
        "DATABASE_URL",
        # Fallback: SQLite in-memory — no external service needed locally
        "sqlite:///:memory:",
    )

    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": db_url,
        }
    )
    yield application


@pytest.fixture(scope="session")
def client(app):
    """Return a test client for the whole session."""
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_db(app):
    """Wipe every table before each individual test for isolation."""
    with app.app_context():
        _db.session.remove()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
