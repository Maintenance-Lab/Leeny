from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField, TextAreaField

class ProductForm(FlaskForm):
    article_number = StringField('Article number', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price_when_bought = IntegerField('Price when bought', validators=[DataRequired()])
    description = TextAreaField('Description')
    EAN = StringField('EAN')
    url = StringField('url')
    manufacturer_id = IntegerField('Manufacturer ID', validators=[DataRequired()])
    category_id = IntegerField('Category ID', validators=[DataRequired()])
    vendor_id = IntegerField('Vendor ID', validators=[DataRequired()])
