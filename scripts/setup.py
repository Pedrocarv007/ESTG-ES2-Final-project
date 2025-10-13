#!/usr/bin/env python3
"""
Setup script for StudyHub AI
Initializes the application and creates necessary directories and files.
"""

import os
import sys

def create_directories():
    """Create necessary directories for the application."""
    directories = [
        'logs',
        'instance',
        'uploads',
        'app/static/uploads'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def setup_environment():
    """Setup environment file if it doesn't exist."""
    if not os.path.exists('.env'):
        with open('.env.example', 'r') as example:
            content = example.read()
        
        with open('.env', 'w') as env_file:
            env_file.write(content)
        
        print("Created .env file from example. Please update with your settings.")

def main():
    """Main setup function."""
    print("Setting up StudyHub AI...")
    
    create_directories()
    setup_environment()
    
    print("Setup completed successfully!")
    print("Next steps:")
    print("1. Update .env file with your configuration")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Initialize database: flask db upgrade")
    print("4. Run application: python run.py")

if __name__ == "__main__":
    main()