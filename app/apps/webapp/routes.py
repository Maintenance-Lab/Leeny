# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from urllib.parse import urljoin

import requests
from apps.config import API_GENERATOR
from apps.webapp import blueprint
from flask import current_app, flash, render_template, redirect, url_for, request, session
from flask_login import login_required
from jinja2 import TemplateNotFound
import http
from datetime import datetime
from apps.authentication.forms import CreateAccountForm
from apps.authentication.models import Users
from flask_login import current_user
from apps import db, login_manager
from apps.webapp.models import *
from apps.authentication.models import *
from apps.webapp.forms import *
# staat nog niet goed ivm verplaatsing ivm api traag
from apps.api.forms import *
from sqlalchemy import update


@blueprint.route('/index')
# @login_required
def index():
    return render_template('app/index.html', segment='index', API_GENERATOR=len(API_GENERATOR))

@blueprint.route('/barcode-scanning')
def barcode_scanning():
    return render_template('app/barcode-scanning.html', API_GENERATOR=len(API_GENERATOR))

@blueprint.route('/start', methods=["GET", "POST"])
def start():
    [session.pop(key) for key in list(session.keys()) if key != '_flashes']
    if request.method == "POST":
        flash({'text':'123'}, 'Login')
        # Login scanner activeren
    return render_template('app/start.html', API_GENERATOR=len(API_GENERATOR))


@blueprint.route('/borrow', methods=["GET","POST"])
# @login_required
def borrow():
    if request.method == "POST":
        flash({'text':'123'}, 'cancel')
    return render_template('app/borrow.html')


@blueprint.route('/home')
# @login_required
def home():
    return render_template('app/home.html', segment='home')

@blueprint.route('/inventory')
# @login_required
def inventory():
    # Add pagination
    return render_template('app/inventory.html', segment='inventory')

@blueprint.route('/return')
# @login_required
def returns():
    # Add pagination
    return render_template('app/return.html', segment='return')

@blueprint.route('/settings' , methods=["GET","POST"])
# @login_required
def settings():
    create_account_form = CreateAccountForm(request.form)
    all_objects = Users.query.filter_by(id=session['_user_id'])
    data = {'data':[{'id': obj.id, **UsersForm(obj=obj).data} for obj in all_objects]}
    if request.method == "POST":
        test = Users.query.filter_by(id=session['_user_id']).update(dict(fullname=request.form['fullname']))
        test2 = Users.query.filter_by(id=session['_user_id']).update(dict(email=request.form['email']))
        test3 = Users.query.filter_by(id=session['_user_id']).update(dict(study=request.form['study']))
        test4 = Users.query.filter_by(id=session['_user_id']).update(dict(faculty=request.form['faculty']))
        test5 = Users.query.filter_by(id=session['_user_id']).update(dict(role=request.form['role']))
        db.session.commit()
        flash({'category':'success', 'title': 'Changes saved!', 'text': '.'}, 'General')
        return redirect(url_for('webapp_blueprint.settings'))
    return render_template('app/settings.html', segment='settings', data=data, session=session, form=create_account_form)


@blueprint.route('/item/<int:id>')
def item(id):
    api_url = urljoin(current_app.config["API_ENDPOINT"], f"item/{id}")
    response = requests.get(url=api_url, timeout=1)
    response.raise_for_status()

    result = response.json()
    return render_template('app/item.html', data=result, segment='inventory')

@blueprint.route('/new_item/')
@blueprint.route('/item/<int:id>/edit')
# @login_required
def new_item(id = None):
    result = None
    try:
        api_url = urljoin(current_app.config["API_ENDPOINT"], f"item/{id}")
        response = requests.get(url=api_url, timeout=1)
        response.raise_for_status()

        result = response.json()
        
    except:
        pass

    return render_template('app/new-item.html', data=result, segment='inventory')


@blueprint.route('/<template>')
# @login_required
def route_template(template):
    print('route_template: ', template)
    try:
        model_name = template if not template.endswith('.html') else template[:-5]
        try:
            api_url = urljoin(current_app.config["API_ENDPOINT"], model_name)
            print('yup:', api_url)
            response = requests.get(url=api_url, timeout=1)
            response.raise_for_status()

            # Convert timestamp to datetime for created_at and updated_at
            result = response.json()
            for item in result['data']:
                if 'created_at_ts' in item and 'updated_at_ts' in item:
                        item['created_at_dt'] = datetime.fromtimestamp(item['created_at_ts']).strftime('%Y-%m-%d %H:%M')
                        item['created_at_dt'] = datetime.fromtimestamp(item['updated_at_ts']).strftime('%Y-%m-%d %H:%M')

            return render_template("app/" + template, data=result)

        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code
        except requests.exceptions.ConnectionError:
            status_code = 500
        except requests.exceptions.Timeout:
            status_code = 408
        except requests.exceptions.RequestException:
            status_code = 408
        error_message = "API error: " + http.HTTPStatus(status_code).phrase

        print('API url:', api_url)
        print('Error: ', error_message)
        return render_template('app/page-error.html', status_code=status_code, status_text=error_message), status_code

    except TemplateNotFound:
        return render_template('app/page-error.html', status_code=404, status_text=http.HTTPStatus(404).phrase), 404


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
    
### HTMX Routes

@blueprint.route('/inventory/search')
def inventory_search():
    q = request.args.get("q")
    
    all_objects = Product.query \
    .filter(Product.title.contains(q) | Product.description.contains(q) | Manufacturer.name.contains(q)) \
    .join(Manufacturer, Manufacturer.id == Product.manufacturer_id)

    # Legacy code; moet nog vervangen worden met voorbeeld zoals in /inventory/borrowed
    data = {'data':[{'id': obj.id, **ProductForm(obj=obj).data, \
                       'name': obj.manufacturer.name if obj.manufacturer else None} \
                        for obj in all_objects]}

    return render_template('app/inventory-results.html', data=data)

@blueprint.route('/inventory/borrowed')
def inventory_borrowed():
    user_id = request.args.get('user_id')

    select_columns = [Product.id, Product.title, Borrowed.quantity, Borrowed.created_at_ts, Borrowed.estimated_return_date, Manufacturer.name]
    
    all_objects = Borrowed.query \
    .filter(Borrowed.user_id == 1) \
    .join(Product, Product.id == Borrowed.product_id) \
    .join(Manufacturer, Product.id == Manufacturer.id) \
    .with_entities(*select_columns)

    
    data = {'data':[{col.key: obj_field for col, obj_field in zip(select_columns,obj)} for obj in all_objects]}
    print(data)

    return render_template('app/inventory-results.html', data=data)
