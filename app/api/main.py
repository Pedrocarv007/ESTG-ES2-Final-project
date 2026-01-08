from flask import Blueprint, render_template
main_api = Blueprint('main_api', __name__)

@main_api.route('/')
def index():
    return render_template('index.html', active_page='index')

@main_api.route('/about')
def about():
    return render_template('about.html', active_page='about')

@main_api.route('/mimi')
def mimi():
    return render_template('mimi.html', active_page='mimi')
