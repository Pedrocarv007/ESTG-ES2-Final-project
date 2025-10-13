"""
User model for StudyHub AI
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.database import db

class User(UserMixin, db.Model):
    """User model."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    created_groups = db.relationship('Group', backref='creator', lazy='dynamic', foreign_keys='Group.created_by')
    uploaded_materials = db.relationship('Material', backref='uploader', lazy='dynamic')
    ai_conversations = db.relationship('AIConversation', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        """Return user id as string for Flask-Login."""
        return str(self.id)
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }