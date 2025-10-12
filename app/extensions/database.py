"""
SQLAlchemy database extension configuration
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Database instance
db = SQLAlchemy()
migrate = Migrate()

def init_database(app):
    """Initialize database with Flask app."""
    db.init_app(app)
    migrate.init_app(app, db, directory='migrations')
    
    # Create tables in development
    if app.config.get('DEVELOPMENT'):
        with app.app_context():
            db.create_all()
    
    return db