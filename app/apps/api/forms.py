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
