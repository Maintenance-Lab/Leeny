from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired

class BorrowForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', default=1, validators=[DataRequired()])
    returned = IntegerField('Returned', default=0, validators=[DataRequired()])
    estimated_return_date = IntegerField('Estimated return date', default=0, validators=[DataRequired()])
    borrowed_at = IntegerField('Borrowed at', validators=[DataRequired()])
    project = IntegerField('Project', validators=[DataRequired()])
