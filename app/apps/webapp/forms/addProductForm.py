from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class AddProductForm(FlaskForm):
    title = StringField('Product Name', validators=[DataRequired()])
    barcode = StringField('Barcode', validators=[DataRequired()])
    priceBTW = StringField('PriceBTW', validators=[DataRequired()])
    priceNoBTW = StringField('PriceNoBTW', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    quantity_unavailable = IntegerField('Quantity Unavailable', validators=[DataRequired()])
    url = StringField('Website', validators=[DataRequired()])

    document_url = StringField('Document URL')
    description = TextAreaField('Description')
    notes = TextAreaField('Notes')

    category = SelectField('Category', validators=[DataRequired()])
    manufacturer = SelectField('Manufacturer', validators=[DataRequired()])
    vendor = SelectField('Vendor', validators=[DataRequired()])