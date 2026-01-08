"""
Flask extensions initialization
"""
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

# Initialize extensions
login_manager = LoginManager()
csrf = CSRFProtect()
cors = CORS()

def init_extensions(app):
    """Initialize Flask extensions with app."""
    
    # Login Manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para aceder a esta página.'
    login_manager.login_message_category = 'info'
    
    # CSRF Protection
    csrf.init_app(app)
    
    # CORS
    cors.init_app(app, resources={
        r"/mimi/api/*": {
            "origins": ["http://192.168.0.2"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    }, supports_credentials=True)
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))