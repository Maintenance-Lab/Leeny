# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import Email, DataRequired, Optional

# Rfid login and registration


class RfidLoginForm(FlaskForm):
    uid = StringField('Rfid_uid',
                      id='rfid_uid_login',
                      validators=[Optional()])
    username = StringField('Username',
                           id='rfid_username_login',
                           validators=[Optional()])
    password = PasswordField('Password',
                             id='rfid_pwd_login',
                             validators=[Optional()])

    # def validate(self):
    #     if not super().validate():
    #         return False

    #     # Check if uid is provided
    #     if self.uid.data:
    #         # If uid is provided, then username and password are optional
    #         return True

    #     # If uid is not provided, then username and password are required
    #     if not self.username.data or not self.password.data:
    #         raise ValidationError('UID or Username and Password are required.')

    #     return True


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
