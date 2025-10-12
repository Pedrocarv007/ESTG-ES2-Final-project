#!/usr/bin/env python3
"""
StudyHub AI - Entry point for the Flask application
"""
import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app()

if __name__ == '__main__':
    # Development server configuration
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🎓 StudyHub AI - Iniciando aplicação...")
    print(f"📍 Servidor disponível em: http://{host}:{port}")
    print(f"🔧 Modo de desenvolvimento: {debug}")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )