"""
WTF Forms for authentication
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    """Login form."""
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório.'),
        Email(message='Email inválido.')
    ])
    password = PasswordField('Palavra-passe', validators=[
        DataRequired(message='Palavra-passe é obrigatória.')
    ])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    """Registration form."""
    name = StringField('Nome', validators=[
        DataRequired(message='Nome é obrigatório.'),
        Length(min=2, max=64, message='Nome deve ter entre 2 e 64 caracteres.')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório.'),
        Email(message='Email inválido.'),
        Length(max=120, message='Email demasiado longo.')
    ])
    password = PasswordField('Palavra-passe', validators=[
        DataRequired(message='Palavra-passe é obrigatória.'),
        Length(min=6, message='Palavra-passe deve ter pelo menos 6 caracteres.')
    ])
    password2 = PasswordField('Repetir Palavra-passe', validators=[
        DataRequired(message='Confirmação de palavra-passe é obrigatória.'),
        EqualTo('password', message='Palavras-passe não coincidem.')
    ])
    submit = SubmitField('Registar')

    def validate_email(self, email):
        """Validate email is unique."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está registado. Use um email diferente.')

class ChangePasswordForm(FlaskForm):
    """Change password form."""
    current_password = PasswordField('Palavra-passe Atual', validators=[
        DataRequired(message='Palavra-passe atual é obrigatória.')
    ])
    new_password = PasswordField('Nova Palavra-passe', validators=[
        DataRequired(message='Nova palavra-passe é obrigatória.'),
        Length(min=6, message='Palavra-passe deve ter pelo menos 6 caracteres.')
    ])
    new_password2 = PasswordField('Repetir Nova Palavra-passe', validators=[
        DataRequired(message='Confirmação de palavra-passe é obrigatória.'),
        EqualTo('new_password', message='Palavras-passe não coincidem.')
    ])
    submit = SubmitField('Alterar Palavra-passe')