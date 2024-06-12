from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class confirmOrderForm(FlaskForm):
    project = StringField('Project associated with the order', validators=[DataRequired()])
    students = StringField('Students associated with the order')

