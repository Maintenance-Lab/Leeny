from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField, TextAreaField, FileField

class ProductForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    barcode = StringField('Barcode')
    quantity_total = IntegerField('Quantity Available', validators=[DataRequired()])
    quantity_borrowed = IntegerField('Quantity Borrowed')

    priceBTW = IntegerField('Price including BTW')
    priceNoBTW = IntegerField('Price excluding BTW')
    description = TextAreaField('Description')
    url = StringField('url')
    documentation = StringField('Documentation')
    notes = StringField('Notes')
    quantity_unavailable = StringField('Quantity Unavailable')

    manufacturer_id = IntegerField('Manufacturer ID', validators=[DataRequired()])
    category_id = IntegerField('Category ID', validators=[DataRequired()])
    vendor_id = IntegerField('Vendor ID', validators=[DataRequired()])