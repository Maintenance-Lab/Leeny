# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from urllib.parse import urljoin, urlparse
import re

import requests
from apps.config import API_GENERATOR
from apps.webapp import blueprint
from flask import current_app, flash, render_template, redirect, url_for, request, session, jsonify
from flask_login import login_required, login_user
from jinja2 import TemplateNotFound
import http
from datetime import datetime
from apps.authentication.forms import CreateAccountForm, LoginForm
from apps.authentication.models import Users
from flask_login import current_user
from apps import db, login_manager
from apps.webapp.models import *
from apps.authentication.models import *
from apps.webapp.forms import *
# staat nog niet goed ivm verplaatsing ivm api traag
from apps.api.forms import *
from sqlalchemy import update
from sqlalchemy.inspection import inspect
from googlesearch import search
from bs4 import BeautifulSoup
from apps.webapp.imagescraper import get_largest_image



@blueprint.route('/barcode-scanning')
def barcode_scanning():
    return render_template('app/barcode-scanning.html', API_GENERATOR=len(API_GENERATOR))

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
            return render_template('accounts/rfid_login.html',
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
def borrow():
    if request.method == "POST":
        if 'cancel' in request.form:
            flash({'text':'123'}, 'cancel')
    return render_template('app/borrow.html')

@blueprint.route('/borrow/confirm')
def borrow_confirm():
    if session.get('data') == False:
        try:
            data = request.args.get('data')
            session['data'] = data
        except:
            flash({'text':'123'}, 'cancel')
            # Nog aanpassen naar error message
    
    # for item in session['data']:


    return render_template('app/borrow-confirm.html', data=data)

@blueprint.route('/home')
# @login_required
def home():
    return render_template('app/home.html', segment='home')

@blueprint.route('/inventory')
# @login_required
def inventory():
    # Add pagination
    return render_template('app/inventory.html', segment='inventory')

@blueprint.route('/orders')
# @login_required
def orders():
    return render_template('app/orders.html', segment='orders')

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
    result=None
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

    return render_template('app/order-info.html', data=data, segment='orders')

@blueprint.route('/orders/new', methods=["GET", "POST"])
def new_order():
    if request.method == 'POST':
        flash({'text':'Are you sure you want cancel?'}, 'cancel') # to do: sweetalert maken
    if 'cart' not in session:
        session['cart'] = []
    return render_template('app/new-order.html', data=session['cart'], segment='orders')

@blueprint.route('/orders/new/remove/<int:id>', methods=["GET", "POST"])
def new_order_remove(id):
    cart = session['cart']
    session['cart'] = [item for item in cart if item['id'] != id]
    return redirect(url_for('webapp_blueprint.new_order'))

@blueprint.route('/orders/new/item')
def new_order_item():
    if 'cart' not in session:
        session['cart'] = []
    return render_template('app/new-item.html', data=session['cart'], segment='orders')

@blueprint.route('/orders/new/unknown')
def new_order_item_unknown():
    if 'cart' not in session:
        session['cart'] = []
    return render_template('app/new-item-unknown.html', data=session['cart'], segment='orders')

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

    return render_template('app/htmx-results/inventory-results.html', data=data)

@blueprint.route('/inventory/search/small')
def inventory_search_small():
    q = request.args.get("q")

    select_columns = [Product.id, Product.title, Manufacturer.name]
    
    all_objects = Product.query \
    .filter(Product.title.contains(q) | Product.description.contains(q) | Manufacturer.name.contains(q)) \
    .join(Manufacturer, Manufacturer.id == Product.manufacturer_id) \
    .with_entities(*select_columns) \
    .limit(4)

    data = {'data': [{col.key: obj_field for col, obj_field in zip(select_columns, obj)} for obj in all_objects]}

    return render_template('app/htmx-results/inventory-results-small.html', data=data)

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
    
    return render_template('app/htmx-results/borrowed-results.html', data=data)


from datetime import datetime, timedelta

@blueprint.route('/orders/load/<int:load>')
def orders_load(load):
    
    select_columns = [Order.id, Order.created_at_ts, Users.fullname, Order.project]
    all_objects = Order.query \
    .join(Users, Users.id == Order.user_id, isouter = True) \
    .with_entities(*select_columns)

    if load == 1:
        user_id = session["_user_id"]
        all_objects = all_objects.filter(Users.id == user_id)
        
    data = {'data':[{col.key: obj_field for col, obj_field in zip(select_columns,obj)} for obj in all_objects]}

    for item in data['data']:
        timestamp = datetime.fromtimestamp(item['created_at_ts']).date()
        now = datetime.now().date()
        if (timestamp - now) <= timedelta(days=1) and timestamp != now:
            item['created_at_ts'] = 'Yesterday'
        elif timestamp == now:
            item['created_at_ts'] = 'Today'
        else:
            item['created_at_ts'] =  timestamp

    return render_template('app/htmx-results/orders-results.html', data=data)

@blueprint.route('/orders/googlesearch/')
def googlesearchURL():
    q = request.args.get("q")
    data = None

    def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])  # Check if both scheme and netloc (domain) are present
        except ValueError:
            return False
        
    def extract_price(text):
        # Regular expression pattern to match prices
        price_pattern = r'\b(?:\d{1,3}(?:[,\.]\d{3})*(?:[,\.]\d+)?|\d+(?:[,\.]\d+)?)\b'
        
        # Find the first occurrence of a price in the text
        match = re.search(price_pattern, text)

        if match:
            return match.group()
        else:
            return "No price found."


    def get_url_data(url):
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Make data variable
        data = {}
    
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page using Beautiful Soup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the first <h1> tag in the parsed HTML
            first_h1 = soup.find('h1')

            # If <h1> tag is found, return its inner text
            if first_h1:
                data['title'] = first_h1.get_text().strip()
            
            # Define a function to check if a class contains the word "price" and not "cart"
            def contains_price_class(class_name):
                return class_name and 'price' in class_name.lower() and not 'cart' in class_name.lower()
            
            # Find the first element with a class containing the word "price"
            element_with_price_class = soup.find(class_=contains_price_class)
            if element_with_price_class:
                price = extract_price(element_with_price_class.get_text().strip())
                data['price'] = price
            
            # print("Starting image retriever")
            # data['image'] = get_largest_image(url)

            return data
        else:
            return {"error":"Failed to retrieve page information. Please confirm correctness manually."}
        
    if is_valid_url(q):
        data = get_url_data(q)
       
    return render_template('app/htmx-results/googlesearch-results.html', data=data)


@blueprint.route('/manufacturer/dropdown/')
def manufacturer_dropdown():
    all_objects = Manufacturer.query.all()
    data = [obj.name for obj in all_objects]
        
    return render_template('app/htmx-results/manufacturer-dropdown.html', data=data)

@blueprint.route('/category/dropdown/')
def category_dropdown():
    all_objects = Category.query.all()
    data = [obj.name for obj in all_objects]
        
    return render_template('app/htmx-results/category-dropdown.html', data=data)

@blueprint.route('/vendor/dropdown/')
def vendor_dropdown():
    all_objects = Vendor.query.all()
    data = [obj.name for obj in all_objects]
        
    return render_template('app/htmx-results/vendor-dropdown.html', data=data)

