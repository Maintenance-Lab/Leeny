# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime
from flask_login import UserMixin

from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id            = db.Column(db.Integer, primary_key=True)
    fullname      = db.Column(db.String(64), unique=True)
    email         = db.Column(db.String(64), unique=True)
    uid_1         = db.Column(db.String(64), nullable=True)
    uid_2         = db.Column(db.String(64), nullable=True)
    uid_3         = db.Column(db.String(64), nullable=True)
    study         = db.Column(db.String(64), nullable=True)
    faculty       = db.Column(db.String(64), nullable=True)
    role          = db.Column(db.String(16), nullable=True, default='student')

    oauth_github  = db.Column(db.String(100), nullable=True)

    api_token     = db.Column(db.String(100))
    api_token_ts  = db.Column(db.Integer)    
    created_at_ts = db.Column(db.Integer, default=int(datetime.now().timestamp()))
    updated_at_ts = db.Column(db.Integer, default=int(datetime.now().timestamp()), onupdate=int(datetime.now().timestamp()))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.fullname)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    uid_1 = request.form.get('uid_1')
    user = Users.query.filter_by(uid_1=uid_1).first()
    return user if user else None

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(Users)
    