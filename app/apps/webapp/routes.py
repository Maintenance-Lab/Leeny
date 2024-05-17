# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from urllib.parse import urljoin

import requests
from apps.config import API_GENERATOR
from apps.webapp import blueprint
from flask import current_app, flash, render_template, redirect, url_for, request, session
from flask_login import login_required, login_user
from jinja2 import TemplateNotFound
import http
from datetime import datetime
from apps.authentication.forms import CreateAccountForm, LoginForm
from apps.authentication.models import Users
from flask_login import current_user
from apps import db, login_manager
from flask_restx import Resource

from apps.webapp.models import *
from apps.authentication.models import *
from apps.webapp.forms import *
# staat nog niet goed ivm verplaatsing ivm api traag
from apps.api.forms import *
from sqlalchemy import update
from sqlalchemy.inspection import inspect
import json


@blueprint.route('/start', methods=["GET", "POST"])
def start():
    login_form = LoginForm(request.form)

    if request.method == "POST":
        if 'finalize' in request.form:
            # read form data
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

            if user:
                login_user(user)
                flash({'text': '123', 'location': 'home', 'user': user.fullname}, 'Timer')
                return render_template('app/start.html',
                                    form=login_form)

            # Edge cases
            flash({'category':'error', 'title': 'Card not recognized', 'text': 'Please register your card or try a different one.'}, 'General')
            return render_template('app/start.html',
                                msg='Wrong user or password *** edge case ***',
                                form=login_form)
        else:
            flash({'text':'123'}, 'Login')
            return render_template('app/start.html',
                                   form=login_form)

    if current_user.is_authenticated:
        return redirect(url_for('webapp_blueprint.index'))
    else:
        return render_template('app/start.html',
                               form=login_form)


@blueprint.route('/borrow', methods=["GET","POST"])
# @login_required
def post():
    if request.method == "POST":
        # Check if post is from continue button
        if 'continue' in request.form:
            print("form data: ", request.form["borrow_data"])

            # add data to session
            # session["borrow_data"] = request.form["borrow_data"]
            borrow_data = json.loads(request.form["borrow_data"])
            session['addedBarcodes'] = borrow_data

            # create dictionary with names and quantities
            # addedBarcodes = request.form["borrow_data"]
            addedProducts = {}

            for items in borrow_data.items():
                barcode = items[0]
                quantity = items[1]

                if barcode.isdigit():
                    # get product name
                    product = Product.query.filter_by(barcode=barcode).first()
                    product_name = product.title

                    addedProducts[product_name] = quantity

            session["addedProducts"] = addedProducts

            return redirect(url_for('webapp_blueprint.borrow_date'))

        if 'cancel' in request.form:
            flash({'text':'123'}, 'cancel')
    return render_template('app/borrow.html')


@blueprint.route('/borrow-date', methods=["GET","POST"])
# @login_required
def borrow_date():
    form = BorrowDateForm()
    if request.method == "POST":
        # Check if post is from continue button
        if 'continue' in request.form:

            # lookup name with session uid
            user_id = session['_user_id']
            print("User id: ", user_id)

            user = Users.query.filter_by(id=user_id).first()

            if user:
                name = user.fullname
                print("User: ", user.fullname)
                session["name"] = name
            else:
                session["name"] = None

            estimated_return_date = request.form["estimated_return_date"]
            project = request.form["project"]

            # add data to session
            session["estimated_return_date"] = estimated_return_date
            session["project"] = project
            print("Return date: ", estimated_return_date)
            print("Project: ", project)

            return redirect(url_for('webapp_blueprint.borrow_confirm'))

        if 'cancel' in request.form:
            flash({'text':'123'}, 'cancel')
    return render_template('app/borrow-date.html', form=form)


@blueprint.route('/return', methods=["GET","POST"])
# @login_required
def post_return():
    if request.method == "POST":
        # Check if post is from continue button
        if 'continue' in request.form:
            # lookup name with session uid
            user_id = session['_user_id']
            print("User id: ", user_id)

            user = Users.query.filter_by(id=user_id).first()

            if user:
                name = user.fullname
                print("User: ", user.fullname)
                session["name"] = name
            else:
                session["name"] = None

            return redirect(url_for('webapp_blueprint.return_confirm'))

        if 'cancel' in request.form:
            flash({'text':'123'}, 'cancel')
    return render_template('app/return.html')


@blueprint.route('/return-confirm', methods=["GET","POST"])
# @login_required
def return_confirm():
    return render_template('app/return-confirm.html')


@blueprint.route('/borrow/confirm', methods=["GET","POST"])
def borrow_confirm():
    return render_template('app/borrow-confirm.html')

@blueprint.route('/home')
# @login_required
def home():
    return render_template('app/home.html', segment='home')


@blueprint.route('/admin-dashboard')
# @login_required
def admin_dashboard():
    return render_template('app/admin-dashboard.html', segment='admin-dashboard')


@blueprint.route('/admin-inventory')
# @login_required
def admin_inventory():
    return render_template('app/admin-inventory.html', segment='admin-inventory')


@blueprint.route('/add-product')
# @login_required
def admin_add_product():
    return render_template('app/add-product.html', segment='add-product')


@blueprint.route('/inventory')
# @login_required
def inventory():
    # Add pagination
    return render_template('app/inventory.html', segment='inventory')

@blueprint.route('/orders')
# @login_required
def orders():
    # Add pagination
    return render_template('app/orders.html', segment='orders')

@blueprint.route('/borrowed')
# @login_required
def borrows():
    # Add pagination
    return render_template('app/borrowed.html', segment='borrowed')


@blueprint.route('/settings' , methods=["GET","POST"])
# @login_required
def settings():
    create_account_form = CreateAccountForm(request.form)
    all_objects = Users.query.filter_by(id=session['_user_id'])
    data = {'data':[{'id': obj.id, **UsersForm(obj=obj).data} for obj in all_objects]}

    if request.method == "POST":
        if "update_profile" in request.form:
            test = Users.query.filter_by(id=session['_user_id']).update(dict(fullname=request.form['fullname']))
            test2 = Users.query.filter_by(id=session['_user_id']).update(dict(email=request.form['email']))
            test3 = Users.query.filter_by(id=session['_user_id']).update(dict(study=request.form['study']))
            test4 = Users.query.filter_by(id=session['_user_id']).update(dict(faculty=request.form['faculty']))
            # test5 = Users.query.filter_by(id=session['_user_id']).update(dict(role=request.form['role']))
            db.session.commit()
            flash({'category':'success', 'title': 'Changes saved!', 'text': 'Your profile has been updated'}, 'General')
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

@blueprint.route('/orders/<int:order_id>')
def order_info(order_id = None):

    select_columns = [column.name for column in inspect(Ordered).c]
    all_objects = Ordered.query.filter(Ordered.order_id == order_id).all()
    result = []

    for obj in all_objects:
        obj_dict = {}
        for column in obj.__table__.columns.keys():
            obj_dict[column] = getattr(obj, column)
        result.append(obj_dict)

    result_order = []
    order_object = Order.query.filter(Order.ordered_id == order_id).first()
    for obj in [order_object]:
        obj_dict = {}
        for column in obj.__table__.columns.keys():
            obj_dict[column] = getattr(obj, column)
        result_order.append(obj_dict)

    data = {'data': result,'order_data':result_order[0]}

    for item in data['data']:
        timestamp = datetime.fromtimestamp(item['created_at_ts']).date()
        item['created_at_ts'] = timestamp

    data['order_data']['created_at_ts'] = datetime.fromtimestamp(data['order_data']['created_at_ts']).date()

    print(data)

    return render_template('app/order-info.html', data=data, segment='orders')


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
            segment = 'home'

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
    user_id = session['_user_id']

    select_columns = [Product.id, Product.title, Borrowed.quantity, Borrowed.created_at_ts, Borrowed.estimated_return_date, Manufacturer.name]

    all_objects = Borrowed.query \
    .filter(Borrowed.user_id == user_id) \
    .join(Product, Product.id == Borrowed.product_id) \
    .join(Manufacturer, Product.id == Manufacturer.id) \
    .with_entities(*select_columns)


    data = {'data':[{col.key: obj_field for col, obj_field in zip(select_columns,obj)} for obj in all_objects]}

    # return render_template('app/inventory-results.html', data=data)

    return render_template('app/borrowed-results.html', data=data)


from datetime import datetime, timedelta

@blueprint.route('/orders/load')
def orders_load():
    select_columns = [Order.id, Order.created_at_ts, Users.fullname, Order.project]
    all_objects = Order.query \
    .join(Users, Users.id == Order.user_id, isouter = True) \
    .with_entities(*select_columns)

    data = {'data':[{col.key: obj_field for col, obj_field in zip(select_columns,obj)} for obj in all_objects]}

    for item in data['data']:
        timestamp = datetime.fromtimestamp(item['created_at_ts']).date()
        now = datetime.now().date()
        if (timestamp - now) <= timedelta(days=1) and timestamp != now:
            item['created_at_ts'] = 'Yesterday'
        elif timestamp == now:
            item['created_at_ts'] = 'Today'
        else:
            item['created_at_ts'] = timestamp

    return render_template('app/orders-results.html', data=data)
