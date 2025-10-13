"""
Group model for StudyHub AI
"""
from datetime import datetime
from app.config.database import db

# Association table for group members
group_members = db.Table('group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('role', db.String(20), default='member'),  # 'admin' or 'member'
    db.Column('joined_at', db.DateTime, default=datetime.utcnow)
)

class Group(db.Model):
    """Study group model."""
    
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    max_members = db.Column(db.Integer, default=50)
    
    # Relationships
    members = db.relationship('User', secondary=group_members, backref='groups')
    materials = db.relationship('Material', backref='group', lazy='dynamic')
    
    def __repr__(self):
        return f'<Group {self.name}>'
    
    def add_member(self, user, role='member'):
        """Add a user to the group."""
        if not self.is_member(user):
            # Insert into association table
            stmt = group_members.insert().values(
                user_id=user.id,
                group_id=self.id,
                role=role,
                joined_at=datetime.utcnow()
            )
            db.session.execute(stmt)
    
    def remove_member(self, user):
        """Remove a user from the group."""
        if self.is_member(user):
            stmt = group_members.delete().where(
                (group_members.c.user_id == user.id) &
                (group_members.c.group_id == self.id)
            )
            db.session.execute(stmt)
    
    def is_member(self, user):
        """Check if user is a member of the group."""
        return user in self.members
    
    def is_admin(self, user):
        """Check if user is an admin of the group."""
        stmt = db.select(group_members).where(
            (group_members.c.user_id == user.id) &
            (group_members.c.group_id == self.id) &
            (group_members.c.role == 'admin')
        )
        result = db.session.execute(stmt).first()
        return result is not None
    
    def member_count(self):
        """Get number of members in the group."""
        return len(self.members)
    
    def to_dict(self):
        """Convert group to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'subject': self.subject,
            'description': self.description,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'member_count': self.member_count(),
            'is_active': self.is_active
        }