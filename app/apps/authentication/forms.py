# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    uid_1 = StringField('uid_1',
                         id='uid_1_login',
                         validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    fullname = StringField('Full name',
                         id='fullname_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    study = StringField('Study Programme',
                             id='study_create',
                             validators=[])
    faculty = StringField('Faculty',
                             id='faculty_create',
                             validators=[])
    uid_1 = StringField('Card 1',
                             id='card_create',
                             validators=[])
    role = StringField('Role',
                             id='role_create',
                             validators=[])
