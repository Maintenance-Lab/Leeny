from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class VendorForm(FlaskForm):
    vendor_name = StringField('Vendor name', validators=[DataRequired()])
    website = StringField('Website')
