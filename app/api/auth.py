from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.auth.forms import LoginForm, RegistrationForm
from app.models.user import User
from app.config.database import db

auth_api = Blueprint('auth_api', __name__, url_prefix='/auth')

@auth_api.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard_api.dashboard'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and user.check_password(form.password.data):
			login_user(user)
			flash('Login realizado com sucesso!', 'success')
			return redirect(url_for('dashboard_api.dashboard'))
		else:
			flash('Email ou senha inválidos.', 'danger')
	return render_template('auth/login.html', form=form)

@auth_api.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Logout realizado com sucesso!', 'success')
	return redirect(url_for('auth_api.login'))

@auth_api.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard_api.dashboard'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(
			name=form.name.data,
			email=form.email.data
		)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Cadastro realizado com sucesso! Faça login.', 'success')
		return redirect(url_for('auth_api.login'))
	return render_template('auth/register.html', form=form)