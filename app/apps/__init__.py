# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from apps.config import Config
from flask_mail import Mail

# TEST
from flask_apscheduler import APScheduler

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

#
scheduler = APScheduler() 


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'webapp', 'api', 'admin'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

from apps.authentication.oauth import github_blueprint


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)

    app.register_blueprint(github_blueprint, url_prefix="/login") 
    
    configure_database(app)

    mail.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    
    if app.config['DEBUG']:
        app.logger.info('DEBUG            = ' + str(app.config['DEBUG'])             )
        app.logger.info('Page Compression = ' + 'FALSE' if app.config['DEBUG'] else 'TRUE' )
        app.logger.info('DBMS             = ' + app.config['SQLALCHEMY_DATABASE_URI'])
        app.logger.info('ASSETS_ROOT      = ' + app.config['ASSETS_ROOT'] )
        
    return app
