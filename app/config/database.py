"""
Database configuration and initialization
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize database extensions
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize database with Flask app."""

    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models to ensure they are registered with SQLAlchemy
    from app.models import user, group, material
    
    return db