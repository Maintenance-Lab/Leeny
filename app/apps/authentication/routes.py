# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import time
import random
from datetime import datetime

from flask_restx import Resource, Api

import flask
from flask import render_template, redirect, request, url_for, flash, session, jsonify
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from flask_dance.contrib.github import github

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import *
from apps.authentication.models import Users, Scanner

from apps.authentication.util import verify_pass, generate_token

from apps.scripts.email_verif import send_email

from flask import Flask
from flask_mail import Mail, Message

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

@blueprint.route('/get_uid', methods=['GET'])
def get_uid():
    # read uid from card
    scanner = Scanner()
    uid = None
    if scanner.ser.is_open is False:
        # print("Serial port is closed. Opening serial port...")
        scanner.open_serial()
    # print("SCAN ROUND:")
    picca_res = scanner.piccactivate()
    if picca_res.startswith(b'50'):
        uid = scanner.response_parse(picca_res)
        # print(f"\nUID: {uid}\n")
        scanner.set_led()
        scanner.set_buzzer()
    # print("END SCAN ROUND:\n")
    if uid:
        # print("UID found. Exiting...")
        pass
    time.sleep(0.3)
    # close serial
    scanner.ser.close()

    return jsonify({'uid': uid.decode('utf-8') if uid else None})

@blueprint.route('/rfid_login', methods=['GET', 'POST'])
def rfid_login():
    login_form = RfidLoginForm(request.form)

    if request.method == 'POST':

        # read form data
        fullname = request.form['fullname']
        uid = request.form['uid'] or None
        password = request.form['password']

        # Check if uid exists
        if uid:
            print('uid', uid)
            try:
                user = Users.query.filter_by(uid_1=uid).first()
            except Exception as e1:
                print('Error when card scanning:', e1)
            if user is None:
                try:
                    user = Users.query.filter_by(uid_2=uid).first()
                except Exception as e2:
                    print('Error when card scanning:', e2)
            if user is None:
                try:
                    user = Users.query.filter_by(uid_3=uid).first()
                except Exception as e3:
                    print('Error when card scanning:', e3)

        else:
            print('No card used, trying username')
            user = Users.query.filter_by(fullname=fullname).first()

        # Check the password
        if user and password and verify_pass(password, user.password):
            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))
        # Check if user is found but no password is provided
        elif user and not password:
            return render_template('accounts/rfid_login.html',
                               msg='No password provided',
                               form=login_form)
        # Check if uid is provided but no user is found
        elif uid and user is None:
            return render_template('accounts/rfid_login.html',
                               msg='No user found for this card',
                               form=login_form)
        # Check if username is provided but no user is found
        elif fullname and not user:
            return render_template('accounts/rfid_login.html',
                                 msg='No user found with this name',
                                 form=login_form)

        # Authenticated user
        if user:
            login_user(user)
            session['fullname'] = user.fullname
            flash({'text':'123', 'location': 'home', 'user': user.fullname}, 'Timer')
            return render_template('accounts/login.html',
                               form=login_form)

        # Edge cases
        return render_template('accounts/rfid_login.html',
                               msg='Wrong user or password *** edge case ***',
                               form=login_form)

    if current_user.is_authenticated:
        return redirect(url_for('webapp_blueprint.index'))
    else:
        return render_template('accounts/rfid_login.html',
                               form=login_form)


@blueprint.route('/rfid_register', methods=['GET', 'POST'])
def rfid_register():
    create_account_form = RfidCreateAccountForm(request.form)
    if 'register' in request.form:

        fullname = request.form['fullname']
        email = request.form['email']
        uid_1 = request.form['uid_1'] or None

        # Check usename exists
        user = Users.query.filter_by(fullname=fullname).first()
        if user:
            return render_template('accounts/rfid_register.html',
                                   msg='Name already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/rfid_register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # Check if uid exists
        if uid_1:
            try:
                user = Users.query.filter_by(uid_1=uid_1).first()
            except Exception as e1:
                print('Error when card scanning:', e1)
            if user is None:
                try:
                    user = Users.query.filter_by(uid_2=uid_1).first()
                except Exception as e2:
                    print('Error when card scanning:', e2)
            if user is None:
                try:
                    user = Users.query.filter_by(uid_3=uid_1).first()
                except Exception as e3:
                    print('Error when card scanning:', e3)
        # Card already registered
        if user and uid_1:
            return render_template('accounts/rfid_register.html',
                                   msg='Card already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        if uid_1 is None:
            user.uid_1 = uid_1
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('accounts/rfid_register.html',
                               msg='Card registered successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/rfid_register.html', form=create_account_form)

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if flask.request.method == 'POST':

        # read form data
        uid_1 = request.form['uid_1']

        #return 'Login: ' + fullname + ' / ' + password

        # Locate user
        if uid_1:
            try:
                user = Users.query.filter_by(uid_1=uid_1).first()
            except Exception as e1:
                print('Error when card scanning:', e1)
            if user is None:
                try:
                    user = Users.query.filter_by(uid_2=uid_1).first()
                except Exception as e2:
                    print('Error when card scanning:', e2)
            if user is None:
                try:
                    user = Users.query.filter_by(uid_3=uid_1).first()
                except Exception as e3:
                    print('Error when card scanning:', e3)

        # if user is found, log in:
        if user:
            login_user(user)
            session['fullname'] = user.fullname
            session['role'] = user.role
            flash({'text':'123', 'location': 'home', 'user': user.fullname}, 'Timer')
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

        # Check if uid exists
        if uid_1:
            try:
                user = Users.query.filter_by(uid_1=uid_1).first()
            except Exception as e1:
                print('Error when card scanning:', e1)
            if user is None:
                try:
                    user = Users.query.filter_by(uid_2=uid_1).first()
                except Exception as e2:
                    print('Error when card scanning:', e2)
            if user is None:
                try:
                    user = Users.query.filter_by(uid_3=uid_1).first()
                except Exception as e3:
                    print('Error when card scanning:', e3)
        # Card already registered
        if user and uid_1:
            flash({'category':'error', 'title': 'Card already registered!', 'text': 'Use a different card.'}, 'General')
            return render_template('accounts/register.html',
                                   success=False,
                                   form=create_account_form,
                                   step=1)

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


@blueprint.route('/card_reader', methods=['GET', 'POST'])
def card_reader():
    login_form = RfidLoginForm(request.form)

    if request.method == 'POST':
        uid = request.form['uid'] or None

        # Locate user
        if uid:
            try:
                user = Users.query.filter_by(uid_1=uid).first()
            except Exception as e1:
                print('Error when card scanning:', e1)
            if user is None:
                try:
                    user = Users.query.filter_by(uid_2=uid).first()
                    print('user2', user)
                except Exception as e2:
                    print('Error when card scanning:', e2)
            if user is None:
                try:
                    user = Users.query.filter_by(uid_3=uid).first()
                    print('user23', user)
                except Exception as e2:
                    print('Error when card scanning:', e2)

        else:
            print('No card in form')

        # Check if uid is provided but no user is found
        if uid and user is None:
            # return redirect(url_for('authentication_blueprint.rfid_register'),
            #                 msg='No user found for this card, use formal login', form=login_form)
            return render_template('accounts/rfid_login.html',
                               msg='No user found for this card',
                               form=login_form)
            # return redirect(url_for('authentication_blueprint.rfid_register'))

        if user:
            login_user(user)
            flash({'text':'123', 'location': 'home', 'user': user.fullname}, 'Timer')
            return render_template('accounts/rfid_login.html',
                               form=login_form)

        # Edge cases
        return render_template('accounts/rfid_login.html',
                               msg='Wrong user or password *** edge case ***',
                               form=login_form)

    if current_user.is_authenticated:
        return redirect(url_for('webapp_blueprint.index'))
    else:
        return render_template('app/card_reader.html',
                               form=login_form)


@blueprint.route('/email_verification', methods=['GET', 'POST'])
def email_verification():
    login_form = EmailForm(request.form)
    if request.method == 'GET':
        session['email_code'] = random.randint(1000, 9999)
        html = render_template("app/email_send.html", confirm_code=session['email_code'])
        send_email("robinalmekinders@gmail.com", "leeny test", html)

    if request.method == 'POST':
        code_1 = request.form['code_1']
        code_2 = request.form['code_2']
        code_3 = request.form['code_3']
        code_4 = request.form['code_4']

        code = int(f'{code_1}{code_2}{code_3}{code_4}')

        if code == session['email_code']:
            flash({'category':'success', 'title': 'Person Verified!', 'text': 'Your profile was verified'}, 'General')
            print(session)
            return redirect(url_for('webapp_blueprint.borrow_confirm'))
        return render_template('accounts/email_verification.html',
                               msg='Invalid code',
                               form=login_form)
    return render_template('accounts/email_verification.html', form=login_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('authentication_blueprint.login'))


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
