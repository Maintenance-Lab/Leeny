from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField

class ManufacturerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
