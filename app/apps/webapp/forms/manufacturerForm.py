from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField

class ManufacturerForm(FlaskForm):
    manufacturer_name = StringField('Manufacturer name', validators=[DataRequired()])
