"""
Material model for StudyHub AI
"""
from datetime import datetime
import os
from app.config.database import db

class Material(db.Model):
    """Study material model."""
    
    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(255))
    file_name = db.Column(db.String(255))
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)  # in bytes
    
    # Foreign keys
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Material {self.title}>'
    
    def get_file_url(self):
        """Get the URL for accessing the file."""
        from flask import has_request_context, current_app, url_for, g
        # Tenta usar helper do template se disponível
        prefix = ''
        try:
            if has_request_context() and hasattr(g, 'get_url_prefix'):
                prefix = g.get_url_prefix()
            elif has_request_context() and 'get_url_prefix' in current_app.jinja_env.globals:
                prefix = current_app.jinja_env.globals['get_url_prefix']()
            elif has_request_context() and current_app.config.get('USE_PROXY', False):
                prefix = '/studyhubai'
        except Exception:
            prefix = ''
        if self.file_path:
            return f'{prefix}/static/uploads/{os.path.basename(self.file_path)}'
        return None
    
    def get_file_extension(self):
        """Get file extension."""
        if self.file_name:
            return os.path.splitext(self.file_name)[1].lower()
        return ''
    
    def is_image(self):
        """Check if the file is an image."""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        return self.get_file_extension() in image_extensions
    
    def is_document(self):
        """Check if the file is a document."""
        doc_extensions = {'.pdf', '.doc', '.docx', '.txt', '.rtf'}
        return self.get_file_extension() in doc_extensions
    
    def is_presentation(self):
        """Check if the file is a presentation."""
        ppt_extensions = {'.ppt', '.pptx', '.odp'}
        return self.get_file_extension() in ppt_extensions
    
    def format_file_size(self):
        """Format file size in human readable format."""
        if not self.file_size:
            return 'Desconhecido'
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
    
    
    
    def to_dict(self):
        """Convert material to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'file_name': self.file_name,
            'file_type': self.file_type,
            'file_size': self.format_file_size(),
            'file_url': self.get_file_url(),
            'uploaded_by': self.uploaded_by,
            'group_id': self.group_id,
            'created_at': self.created_at.isoformat(),
            'is_image': self.is_image(),
            'is_document': self.is_document(),
            'is_presentation': self.is_presentation()
        }
    


class AIConversation(db.Model):
    """AI conversation history model."""
    
    __tablename__ = 'ai_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    conversation_id = db.Column(db.Integer, nullable=True, index=True)  # Thread/conversa
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    context = db.Column(db.Text)  # Additional context if needed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AIConversation {self.id}>'
    
    def to_dict(self):
        """Convert conversation to dictionary."""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'question': self.question,
            'answer': self.answer,
            'created_at': self.created_at.isoformat()
        }
    

class Folder(db.Model):
    """Folder for organizing materials."""
    __tablename__ = 'folders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationships
    parent = db.relationship('Folder', remote_side=[id], backref='subfolders')
    materials = db.relationship('Material', backref='folder', lazy='dynamic')

    def __repr__(self):
        return f'<Folder {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id,
            'group_id': self.group_id,
            'created_at': self.created_at.isoformat(),
            'subfolders': [sf.to_dict() for sf in self.subfolders],
            'materials': [m.to_dict() for m in self.materials]
        }