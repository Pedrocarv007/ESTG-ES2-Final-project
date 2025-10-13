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
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))