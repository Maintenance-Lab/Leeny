from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class VendorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    website = StringField('Website')
