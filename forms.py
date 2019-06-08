from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField

class SubmitForm(FlaskForm):
	keywords = StringField('Move', validators=[validators.DataRequired()])
	submit = SubmitField('Submit')
