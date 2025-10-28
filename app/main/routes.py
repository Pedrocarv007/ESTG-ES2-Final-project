"""
Main application routes
"""
from flask import render_template, request, jsonify
from app.main import bp

@bp.route('/')
def index():
    """Home page route."""
    return render_template('index.html', active_page='index')

@bp.route('/dashboard')
def dashboard():
    """Dashboard route."""
    return render_template('dashboard.html', active_page='dashboard')

@bp.route('/study')
def study():
    """Study page route."""
    return render_template('study.html', active_page='study')


@bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html', active_page='about')

@bp.route('/contacts')
def contacts():
    """Contact page route."""
    return render_template('contacts.html', active_page='contacts')