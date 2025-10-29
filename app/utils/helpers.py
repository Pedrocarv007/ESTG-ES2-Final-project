# Helper functions
from flask import current_app, url_for

def get_url_prefix():
    """Get the URL prefix for the application based on proxy configuration."""
    if current_app.config.get('USE_PROXY', True):
        return '/studyhubai'
    return ''

def url_for_with_prefix(endpoint, **values):
    """Generate URL for endpoint considering proxy configuration."""
    return url_for(endpoint, **values)