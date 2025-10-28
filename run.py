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
    port = int(os.environ.get('FLASK_PORT', 6002))
    debug = os.environ.get('FLASK_ENV') == 'development'
    use_proxy = os.environ.get('USE_PROXY', 'true').lower() in ['true', 'on', '1']
    
    print("🎓 StudyHub AI - Iniciando aplicação...")
    print(f"📍 Servidor disponível em: http://{host}:{port}")
    print(f"🔧 Modo de desenvolvimento: {debug}")
    print(f"🔄 Modo proxy reverso: {'Ativado' if use_proxy else 'Desativado'}")
    if use_proxy:
        print("📡 URLs com prefixo: /studyhubai")
    else:
        print("📡 URLs diretas (sem prefixo)")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )