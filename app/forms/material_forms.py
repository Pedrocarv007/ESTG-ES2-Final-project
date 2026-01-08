from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class MaterialUploadForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descrição')
    file = FileField('Arquivo', validators=[DataRequired()])
    group_id = SelectField('Grupo', coerce=int)
