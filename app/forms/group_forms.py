from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class GroupCreateForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired(), Length(max=100)])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    goals = TextAreaField('Goals', validators=[Optional(), Length(max=500)])
    max_members = IntegerField('Max Members', validators=[Optional()], description="Deixe em branco para ilimitado.", render_kw={"placeholder": "Deixe em branco para ilimitado"})
    privacy = SelectField('Privacy', choices=[('public', 'Public'), ('private', 'Private')], validators=[Optional(), Length(max=20)])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Create Group')

class GroupEditForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired(), Length(max=100)])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    goals = TextAreaField('Goals', validators=[Optional(), Length(max=500)])
    max_members = IntegerField('Max Members', validators=[Optional()], description="Deixe em branco para ilimitado.", render_kw={"placeholder": "Deixe em branco para ilimitado"})
    is_active = BooleanField('Active')
    submit = SubmitField('Update Group')
