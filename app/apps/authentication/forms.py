# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, EmailField, SelectField)
from wtforms.validators import (
    Email, DataRequired, Optional,
    InputRequired, Regexp, Length,
    )

# Rfid login and registration


class RfidLoginForm(FlaskForm):
    uid = StringField('Rfid_uid',
                      id='rfid_uid_login',
                      validators=[Optional()])
    fullname = StringField('Fullname',
                           id='rfid_fullname_login',
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
    fullname = StringField('Fullname',
                           id='rfid_fullname_create',
                           validators=[DataRequired()])
    email = EmailField('Email',
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
    email = EmailField('Email',
                        id='email_create',
                        validators=[DataRequired(), Email()])
    study = StringField('Study Programme',
                        id='study_create',
                        validators=[DataRequired()])
    faculty = StringField('Faculty',
                          id='faculty_create',
                          validators=[DataRequired()])
    uid_1 = StringField('Card 1',
                        id='card_create',
                        validators=[])
    # role = StringField('Role',
    #                    id='role_create',
    #                    validators=[])
    role = SelectField('Role',
                       id='role_create',
                       choices=[('admin', 'Admin'),
                                ('student', 'Student')],
                        validators=[],
                        default='student')


class EmailForm(FlaskForm):
    code_1 = StringField('Code_1',
                          id='email_code_1',
                          validators=[InputRequired(), Length(min=1, max=1),
                                      Regexp('[0-9]')])
    code_2 = StringField('Code_2',
                          id='email_code_2',
                          validators=[InputRequired(), Length(min=1, max=1),
                                      Regexp('[0-9]')])
    code_3 = StringField('Code_3',
                          id='email_code_3',
                          validators=[InputRequired(), Length(min=1, max=1),
                                      Regexp('[0-9]')])
    code_4 = StringField('Code_4',
                          id='email_code_4',
                          validators=[InputRequired(), Length(min=1, max=1),
                                      Regexp('[0-9]')])
