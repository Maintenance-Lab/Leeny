from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired

class OrderedForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    vendor_id = IntegerField('Vendor ID', validators=[DataRequired()])
    ordered = IntegerField('Ordered', default=0, validators=[DataRequired()])
    delivered = IntegerField('Delivered', default=0, validators=[DataRequired()])
    ordered_at = IntegerField('Ordered at', validators=[DataRequired()])

