# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import Email, DataRequired, Optional

# Rfid login and registration


class RfidLoginForm(FlaskForm):
    username = StringField('Username',
                           id='rfid_username_login',
                           validators=[Optional()])
    password = PasswordField('Password',
                             id='rfid_pwd_login',
                             validators=[Optional()])
    uid = StringField('Rfid_uid',
                        id='rfid_uid_login',
                        validators=[Optional()])
    


class RfidCreateAccountForm(FlaskForm):
    username = StringField('Username',
                           id='rfid_username_create',
                           validators=[DataRequired()])
    email = StringField('Email',
                        id='rfid_email_create',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='rfid_pwd_create',
                             validators=[DataRequired()])
    uid_1 = StringField('Rfid_uid',
                        id='rfid_uid_create',
                        validators=[Optional()])

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                           id='username_login',
                           validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                           id='username_create',
                           validators=[DataRequired()])
    email = StringField('Email',
                        id='email_create',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
