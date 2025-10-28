"""
StudyHub AI Flask Application Factory
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

def create_app(config_name=None):
    """Create and configure Flask application."""
    
    # Create Flask app
    app = Flask(__name__, static_url_path="/studyhubai/static", static_folder="static")
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Configure for proxy reverse
    if app.config.get('USE_PROXY', True):
        app.static_url_path = "/studyhubai/static"
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Initialize extensions
    from app.extensions import init_extensions
    init_extensions(app)
    
    # Initialize database
    from app.config.database import init_db
    init_db(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register template helpers
    register_template_helpers(app)
    
    # Setup logging
    setup_logging(app)
    
    # Error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check_root():
        return {'status': 'healthy', 'service': 'StudyHub AI'}, 200
    
    return app


def register_blueprints(app):
    """Register application blueprints."""
    
    # Get prefix from config
    use_proxy = app.config.get('USE_PROXY', True)
    prefix = '/studyhubai' if use_proxy else ''
    
    # Main routes
    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix=prefix)
    
    # Authentication routes
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix=f'{prefix}/auth')
    
    # API routes
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix=f'{prefix}/api')
    
    # Health check endpoint with prefix
    @app.route(f'{prefix}/health')
    def health_check():
        return {'status': 'healthy', 'service': 'StudyHub AI'}, 200


def register_template_helpers(app):
    """Register template helper functions."""
    
    from app.utils.helpers import get_url_prefix
    
    @app.context_processor
    def inject_helpers():
        return {
            'get_url_prefix': get_url_prefix
        }


def register_error_handlers(app):
    """Register error handlers."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Página não encontrada'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return {'error': 'Erro interno do servidor'}, 500
    
    @app.errorhandler(413)
    def file_too_large(error):
        return {'error': 'Ficheiro demasiado grande'}, 413


def setup_logging(app):
    """Setup application logging."""
    
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Setup file handler
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.info('StudyHub AI startup')
