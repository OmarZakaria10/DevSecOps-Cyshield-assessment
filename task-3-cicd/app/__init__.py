"""
Flask application factory.
Creates and configures the Flask app instance.
"""

from flask import Flask
from .database import db
from .routes import api_bp


def create_app(config=None):
    """Create a Flask application instance.

    Args:
        config (dict, optional): Override configuration values.

    Returns:
        Flask: Configured Flask application.
    """
    app = Flask(__name__)

    # Default configuration — real secrets live in environment variables,
    # never hard-coded here.
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=(
            "postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s"
            % {
                "user": __import__("os").getenv("DB_USER", "postgres"),
                "password": __import__("os").getenv("DB_PASSWORD", "postgres"),
                "host": __import__("os").getenv("DB_HOST", "localhost"),
                "port": __import__("os").getenv("DB_PORT", "5432"),
                "db": __import__("os").getenv("DB_NAME", "taskdb"),
            }
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTING=False,
    )

    if config:
        app.config.update(config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app
