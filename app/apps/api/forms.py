from wtforms import Form
from wtforms_alchemy import model_form_factory
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length

from apps.webapp.models import *
from apps.authentication.models import Users

ModelForm = model_form_factory(Form)

class UsersForm(ModelForm):
    class Meta:
        model = Users
        exclude = ['oauth_github', 'api_token', 'api_token_ts']


class BorrowDateForm(FlaskForm):
    user_id = HiddenField('ID')
    borrow_data = HiddenField('Borrow Data')

    project = StringField('Project', validators=[DataRequired(), Length(max=100)], render_kw={"type": "text"})
    estimated_return_date = DateField('Estimated Return Date', format='%d-%m-%Y', validators=[DataRequired()], render_kw={"placeholder": "DD-MM-YYYY"})
    submit = SubmitField('Borrow')
