from wtforms import Form
from wtforms_alchemy import model_form_factory
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

from apps.webapp.models import *
from apps.authentication.models import Users

ModelForm = model_form_factory(Form)

class UsersForm(ModelForm):
    class Meta:
        model = Users
        exclude = ['oauth_github', 'api_token', 'api_token_ts']


# class ProductForm(ModelForm):
#     class Meta:
#         model = Product
#         exclude = ['barcode', 'price_when_bought', 'description', 'url', 'documentation', 'notes', 'created_at_ts']
#         # The things that remain are: title, item_uid, quantity_total, quantity_borrowed, quantity_unavailable


class ProductForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    item_uid = StringField('Item UID', validators=[DataRequired()])
    quantity_total = IntegerField('Total Quantity', validators=[DataRequired()])
    quantity_borrowed = IntegerField('Borrowed Quantity', validators=[DataRequired()])
    quantity_unavailable = IntegerField('Unavailable Quantity', validators=[DataRequired()])



