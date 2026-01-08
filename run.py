#!/usr/bin/env python3
"""
StudyHub AI - Entry point for the Flask application
"""
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
from app import create_app

# Create Flask app
app = create_app()

if __name__ == '__main__':
    # Development server configuration
    host = os.environ.get('FLASK_HOST')
    port = int(os.environ.get('FLASK_PORT'))
    debug = os.environ.get('FLASK_ENV') 
    use_proxy = os.environ.get('USE_PROXY')
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
        debug=debug,
        threaded=True
    )