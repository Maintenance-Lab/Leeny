# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json
from datetime import datetime

from flask_restx import Resource, Api

import flask
from flask import render_template, redirect, request, url_for, flash, session
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from flask_dance.contrib.github import github

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass, generate_token

# Bind API -> Auth BP
api = Api(blueprint)

@blueprint.route('/')
def route_default():
    return redirect(url_for('webapp_blueprint.start'))

# Login & Registration

@blueprint.route("/github")
def login_github():
    """ Github login """
    if not github.authorized:
        return redirect(url_for("github.login"))

    res = github.get("/user")
    return redirect(url_for('webapp_blueprint.index'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if flask.request.method == 'POST':  

        # read form data
        uid_1 = request.form['uid_1']

        #return 'Login: ' + fullname + ' / ' + password

        # Locate user
        user = Users.query.filter_by(uid_1=uid_1).first()

        # Check the password
        # if user and verify_pass(password, user.password):
        if user:
            login_user(user)
            flash({'text':'123', 'location': 'index', 'user': user.fullname}, 'Timer')
            return render_template('accounts/login.html',
                               form=login_form) 

        else:
            # Something (user or pass) is not ok
            return render_template('accounts/login.html',
                                msg='User not registered',
                                form=login_form)

    return render_template('accounts/login.html',
                               form=login_form) 


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)

    if 'step2' in request.form:

        fullname = request.form['fullname']
        email = request.form['email']


        # Check usename exists
        user = Users.query.filter_by(fullname=fullname).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Your account is already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='This email is already registered',
                                   success=False,
                                   form=create_account_form)

        session['fullname'] = fullname
        session['email'] = email

        return render_template('accounts/register.html',
                               form=create_account_form,
                               step=2)

    if 'step3' in request.form:
        study = request.form['study']
        faculty = request.form['faculty']

        session['study'] = study
        session['faculty'] = faculty
        flash({'text':'123'}, 'Login')
        # Register card scanner activeren

        return render_template('accounts/register.html',
                               form=create_account_form,
                               step=3)
    if 'finalize' in request.form:
        uid_1 = request.form['uid_1']

        user = Users(
            fullname =session['fullname'],
            email = session['email'],
            study = session['study'],
            faculty = session['faculty'],
            uid_1 = uid_1)

        db.session.add(user)
        db.session.commit()

        logout_user()
        [session.pop(key) for key in list(session.keys()) if key != '_flashes']

        flash({'category':'success', 'title': 'Account registered!', 'text': 'You can now log in using your card.'}, 'General')
        return redirect('/start')


    else:
        return render_template('accounts/register.html', form=create_account_form, step=1, session=session)

@api.route('/login/jwt/', methods=['POST'])
class JWTLogin(Resource):
    def post(self):
        try:
            data = request.form

            if not data:
                data = request.json

            if not data:
                return {
                           'message': 'fullname or password is missing',
                           "data": None,
                           'success': False
                       }, 400
            # validate input
            
            user = Users.query.filter_by(uid_1=data.get('uid_1')).first()
            # if user and verify_pass(data.get('password'), user.password):
            if user:
                try:

                    # Empty or null Token
                    if not user.api_token or user.api_token == '':
                        user.api_token = generate_token(user.id)
                        user.api_token_ts = int(datetime.utcnow().timestamp())
                        db.session.commit()

                    # token should expire after 24 hrs
                    return {
                        "message": "Successfully fetched auth token",
                        "success": True,
                        "data": user.api_token
                    }
                except Exception as e:
                    return {
                               "error": "Something went wrong",
                               "success": False,
                               "message": str(e)
                           }, 500
            return {
                       'message': 'fullname or password is wrong',
                       'success': False
                   }, 403
        except Exception as e:
            return {
                       "error": "Something went wrong",
                       "success": False,
                       "message": str(e)
                   }, 500


@blueprint.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('authentication_blueprint.login')) 

@blueprint.route('/card_reader/')
def card_reader():

    data = {'uid': 123} # hier data invoegen
    return render_template('app/card-reader.html', data=data)

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('app/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('app/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('app/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('app/page-500.html'), 500
