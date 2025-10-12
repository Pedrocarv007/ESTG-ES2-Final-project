"""
Main application routes
"""
from flask import render_template, request, jsonify
from app.main import bp

@bp.route('/')
def index():
    """Home page route."""
    return render_template('index.html')

@bp.route('/dashboard')
def dashboard():
    """Dashboard route."""
    return render_template('dashboard/index.html')

@bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html')

@bp.route('/contact')
def contact():
    """Contact page route."""
    return render_template('contact.html')