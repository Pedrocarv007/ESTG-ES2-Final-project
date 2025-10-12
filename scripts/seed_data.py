#!/usr/bin/env python3
"""
Seed data script for StudyHub AI
Creates sample data for testing and development.
"""

from app import create_app
from app.extensions.database import db
from app.models.user import User
from app.models.group import Group
from app.models.material import Material

def create_sample_users():
    """Create sample users."""
    users = [
        {
            'name': 'Pedro Carvalho',
            'email': 'pedro@studyhub.com',
            'password': 'password123'
        },
        {
            'name': 'Lara Jennifer',
            'email': 'lara@studyhub.com',
            'password': 'password123'
        },
        {
            'name': 'Thaissa',
            'email': 'thaissa@studyhub.com',
            'password': 'password123'
        },
        {
            'name': 'Sarah',
            'email': 'sarah@studyhub.com',
            'password': 'password123'
        }
    ]
    
    for user_data in users:
        user = User(
            name=user_data['name'],
            email=user_data['email']
        )
        user.set_password(user_data['password'])
        db.session.add(user)
    
    print(f"Created {len(users)} sample users")

def create_sample_groups():
    """Create sample study groups."""
    groups = [
        {
            'name': 'Engenharia de Software II',
            'subject': 'Software Engineering',
            'description': 'Grupo de estudo para a disciplina de ES2'
        },
        {
            'name': 'Matemática Discreta',
            'subject': 'Mathematics',
            'description': 'Resolução de exercícios de matemática discreta'
        },
        {
            'name': 'Bases de Dados',
            'subject': 'Database',
            'description': 'Estudo de SQL e modelação de dados'
        }
    ]
    
    first_user = User.query.first()
    
    for group_data in groups:
        group = Group(
            name=group_data['name'],
            subject=group_data['subject'],
            description=group_data['description'],
            created_by=first_user.id
        )
        db.session.add(group)
    
    print(f"Created {len(groups)} sample groups")

def main():
    """Main seeding function."""
    app = create_app()
    
    with app.app_context():
        print("Seeding database with sample data...")
        
        # Create tables if they don't exist
        db.create_all()
        
        # Add sample data
        create_sample_users()
        create_sample_groups()
        
        # Commit changes
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == "__main__":
    main()