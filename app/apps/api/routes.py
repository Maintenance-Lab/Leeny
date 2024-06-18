import json
import random

from apps.api import blueprint
from apps.api.forms import *
from apps.authentication.decorators import token_required
from apps.authentication.models import Users
from apps.webapp.models import *
from apps.webapp.forms import *
from flask import request, jsonify, Response, session, flash, render_template
from flask_restx import Api, Resource
from werkzeug.datastructures import MultiDict
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from apps.authentication.util import verify_pass
from apps.email import send_email


api = Api(blueprint)

@api.route('/changeCardUID', methods=['POST'])
class changeCardUID(Resource):
    def post(self):
        data = request.get_json()
        print("DATA ---------------------:", data)
        card = data['card']
        new_uid = data['new_uid']

        # Controleren of er een gebruiker bestaat met uid_1 gelijk aan new_uid
        exists_1 = Users.query.filter_by(uid_1=new_uid).first() is not None
        # Controleren of er een gebruiker bestaat met uid_2 gelijk aan new_uid
        exists_2 = Users.query.filter_by(uid_2=new_uid).first() is not None
        # Controleren of er een gebruiker bestaat met uid_3 gelijk aan new_uid
        exists_3 = Users.query.filter_by(uid_3=new_uid).first() is not None

        # Print de resultaten
        print(exists_1, exists_2, exists_3)

        if not (exists_1 or exists_2 or exists_3):
            # Get the user_id from the session
            user_id = session['_user_id']
            user = Users.query.filter_by(id=user_id).first()

            # Change uid to new uid
            if card == '1':
                user.uid_1 = new_uid
            elif card == '2':
                user.uid_2 = new_uid
            elif card == '3':
                user.uid_3 = new_uid

            # Save changes to database
            db.session.commit()

            output = {
                'message': f'Card UID updated',
                'success': True
            }

        else:
            output = {
                'message': f'Card UID already exists',
                'success': False
            }


        return output, 200

@api.route('/authenticate_admin', methods=['GET', 'POST'])
class AuthenticateAdmin(Resource):
    def post(self):
        data = request.get_json()

        if data['uid']:
            uid = data['uid']
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

            if user:
                print("User role: ", user.role)
                if user.role == 'admin':
                    return {'authenticated': True, 'role': 'admin'}
                else:
                    return {'authenticated': True, 'role': 'student'}

        return {'authenticated': False}

    def get(self):
        user_id = session['_user_id']

        user = Users.query.filter_by(id=user_id).first()
        if user.role == 'admin':
            return {'authenticated': True, 'role': 'admin'}

        return {'authenticated': False}

@api.route('/get_barcode', methods=['POST'])
class GetBarcode(Resource):
    def post(self):
        barcodes = session.get('barcodes', [])
        print("Getting barcodes: ", barcodes)
        return {'barcodes': barcodes}, 200

@api.route('/clear_barcode', methods=['POST'])
class ClearBarcode(Resource):
    def post(self):
        session['barcodes'] = []
        return {'message': 'Barcodes cleared'}, 200

@api.route('/clear_project_date', methods=['POST'])
class ClearProjectDate(Resource):
    def post(self):
        session['project'] = ''
        session['estimated_return_date'] = ''
        return {'message': 'Project date cleared'}, 200

@api.route('/get_project_date', methods=['POST'])
class GetProjectDate(Resource):
    def post(self):
        project = session.get('project', '')
        estimated_return_date = session.get('estimated_return_date', '')
        return {'project': project, 'estimated_return_date': estimated_return_date}, 200

@api.route('/set_project_date', methods=['POST'])
class SetProjectDate(Resource):
    def post(self):
        data = request.get_json()
        project = data['project']
        estimated_return_date = data['estimated_return_date']

        session['project'] = project
        session['estimated_return_date'] = estimated_return_date
        print("Project date set")
        return {'message': 'Project date set'}, 200

@api.route('/borrow', methods=['POST'])
class Borrow(Resource):
    def post(self):
        # Get the barcode data from the request
        data = request.get_json()
        barcode = data['barcode']

        product = Product.query.filter_by(barcode=barcode.upper()).first()
        if product is None:
            product = Product.query.filter_by(title=barcode).first()

        if product:
            print("PRODUCT TILE: ", product.title)
            if product.barcode:
                print("PRODUCT BARCODE: ", product.barcode)
                barcode = product.barcode
            title = product.title
            quantity_total = product.quantity_total
            quantity_unavailable = product.quantity_unavailable
            quantity_borrowed = product.quantity_borrowed

            quantity = quantity_total - quantity_unavailable - quantity_borrowed
            print("sending this barcode: ", barcode)
            if quantity > 0:
                # Product found
                output = {
                    'barcode': barcode,
                    'name': title,
                    'quantity': quantity,
                    'message': f'Product found',
                    'success': True
                }
            else:
                # Product not available
                output = {
                    'barcode': barcode,
                    'name': title,
                    'message': f'Product not available',
                    'success': False
                }
        else:
            # Product not found
            output = {
                'barcode': barcode,
                'message': f'Product not found',
                'success': False
            }

        return output, 200

@api.route('/borrow/add_to_cart', methods=['POST'])
class borrow_add_to_cart(Resource):
    def post(self):
        data = request.get_json()
        itemName = data['itemName']
        product = Product.query.filter_by(title=itemName).first()
        quantity = product.quantity_total - product.quantity_borrowed
        data =[]
        if 'borrow_cart' in session:
            data = session['borrow_cart']

        data.append({'title':product.title, 'id':product.id, 'quantity':quantity})
        session['borrow_cart'] = data
        return data, 200

@api.route('/borrow2', methods=['POST'])
class Borrow2(Resource):
    def post(self):
        addedBarcodes = session['addedBarcodes']
        project = session['project']
        return_date = session['estimated_return_date']

        for items in addedBarcodes.items():
            print("barcode: ", items[0], "quantity: ", items[1])
            barcode = items[0]
            quantity = items[1]

            # If barcode is an int
            if barcode != 'null':
                # Add 1 to quantity borrowed
                product = Product.query.filter_by(barcode=barcode).first()
                if product is None:
                    product = Product.query.filter_by(title=barcode).first()

                if product:
                    product.quantity_borrowed += quantity

                    # Add borrow entry to borrowed table
                    user_id = session['_user_id']
                    borrow = Borrowed(user_id=user_id,
                                    product_id=product.id,
                                    quantity=quantity,
                                    project=project,
                                    estimated_return_date=return_date
                                    )
                    print("ADD TO TABLE: ", borrow)

                    # Check if the user already has a borrowed item with the same product_id
                    existing_borrow = Borrowed.query.filter_by(user_id=user_id, product_id=product.id).first()
                    if existing_borrow:
                        existing_borrow.quantity += quantity
                        print("Existing borrow found. Quantity updated.")
                    else:
                        db.session.add(borrow)
                        print("New borrow added to table.")

        # Save changes to database
        print("COMMITING CHANGES -------------------------------")
        db.session.commit()

        session['barcodes'] = []

        # Send email to users
        user_id = session['_user_id']
        user = Users.query.filter_by(id=user_id).first()
        email = user.email

        borrowed_date = datetime.today().strftime('%d-%m-%Y')
        timestamp = datetime.fromtimestamp(int(session['estimated_return_date'])).strftime('%d-%m-%Y')
        html = render_template('app/email_borrow_overview.html', timestamp=timestamp, borrowed_date=borrowed_date)
        send_email(email, "Borrow overview", html)

@api.route('/return', methods=['POST'])
class Return(Resource):
    def post(self):
        # Get the barcode data from the request
        data = request.get_json()
        barcode = data['barcode']

        product = Product.query.filter_by(barcode=barcode.upper()).first()
        if product is None:
            product = Product.query.filter_by(title=barcode).first()

        if product:
            if product.barcode:
                barcode = product.barcode

            title = product.title

            # quantity for borrowed from user
            user_id = session['_user_id']
            borrow = Borrowed.query.filter_by(user_id=user_id, product_id=product.id).first()

            if borrow:
                # Product found
                output = {
                    'barcode': barcode,
                    'name': title,
                    'quantity': borrow.quantity,
                    'message': f'Product found',
                    'success': True
                }
            else:
                # Product not borrowed
                output = {
                    'barcode': barcode,
                    'message': f'Product not borrowed',
                    'success': False
                }

        else:
            # Product not found
            output = {
                'barcode': barcode,
                'message': f'Product not found',
                'success': False
        }

        return output, 200

@api.route('/return-confirm', methods=['POST'])
class ReturnConfirm(Resource):
    def post(self):
        return_data = session['addedBarcodes']

        for items in return_data.items():
            print("barcode: ", items[0], "quantity: ", items[1])
            barcode = items[0]
            quantity = items[1]

            # If barcode is an int
            if barcode != 'null':
                # Subtract from quantity borrowed
                product = Product.query.filter_by(barcode=barcode).first()
                product.quantity_borrowed -= quantity

                # Change/remove borrow entry from borrowed table
                user_id = session['_user_id']
                borrow = Borrowed.query.filter_by(user_id=user_id, product_id=product.id).first()
                borrow.quantity -= quantity
                borrow.returned += quantity

        # Save changes to database
        print("COMMITING CHANGES -------------------------------")
        db.session.commit()

        session['barcodes'] = []

        # Send email to users
        user_id = session['_user_id']
        user = Users.query.filter_by(id=user_id).first()
        email = user.email

        returned_timestamp = datetime.today().strftime('%d-%m-%Y')
        html = render_template('app/email_return_overview.html', returned_timestamp=returned_timestamp)
        send_email(email, "Return overview", html)

@api.route('/admin-login', methods=['POST'])
class AdminLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']

        user = Users.query.filter_by(email=email).first()

        if user is not None and user.role == 'admin':
            if verify_pass(password, user.password):
                session['_user_id'] = user.id
                session['email'] = user.email
                session['role'] = user.role
                session['fullname'] = user.fullname

                output = {
                    'message': f'Login successful',
                    'success': True
                }
        else:
            output = {
                'message': f'Login failed',
                'success': False
            }

        return output, 200

@api.route('/get-options')
class GetOptions(Resource):
    def get(self):
        # Get all manufacturers, categories, and vendors
        manufacturers = [manufacturer.manufacturer_name for manufacturer in Manufacturer.query.all()]
        categories = [category.category_name for category in ProductCategory.query.all()]
        vendors = [vendor.vendor_name for vendor in Vendor.query.all()]

        # sort alphabetically
        manufacturers.sort()
        categories.sort()
        vendors.sort()

        return {
            'success': True,
            'manufacturers': manufacturers,
            'categories': categories,
            'vendors': vendors
        }

@api.route('/manufacturer/dropdown', methods=['GET'])
class GetManufacturers(Resource):
    def get(self):
        manufacturers = Manufacturer.query.all()
        data = [{'id': m.id, 'name': m.manufacturer_name} for m in manufacturers]
        return jsonify(data)

@api.route('/category/dropdown', methods=['GET'])
class GetCategories(Resource):
    def get(self):
        categories = ProductCategory.query.all()
        data = [{'id': c.id, 'name': c.category_name} for c in categories]
        return jsonify(data)

@api.route('/vendor/dropdown', methods=['GET'])
class GetVendors(Resource):
    def get(self):
        vendors = Vendor.query.all()
        data = [{'id': v.id, 'name': v.vendor_name} for v in vendors]
        return jsonify(data)

@api.route('/add-product', methods=['POST'])
class AddProduct(Resource):
    def post(self):
        data = request.form.to_dict(flat=True)
        print("DATA: ", data)

        # Get manufacturer/category/vendor id or create new entry
        manufacturer_name = data['manufacturer']
        manufacturer = Manufacturer.query.filter_by(manufacturer_name=manufacturer_name).first()
        if not manufacturer:
            manufacturer = Manufacturer(manufacturer_name=manufacturer_name)
            db.session.add(manufacturer)
            db.session.commit()

        category_name = data['category']
        category = ProductCategory.query.filter_by(category_name=category_name).first()
        if not category:
            category = ProductCategory(category_name=category_name)
            db.session.add(category)
            db.session.commit()

        vendor_name = data['vendor']
        vendor = Vendor.query.filter_by(vendor_name=vendor_name).first()
        if not vendor:
            vendor = Vendor(vendor_name=vendor_name)
            db.session.add(vendor)
            db.session.commit()

        priceBTW = 0
        priceNoBTW = 0
        # Check if BTW and No BTW are not '' or None?
        if data['priceBTW'] != '' and data['priceNoBTW'] != '':
            priceBTW = data['priceBTW']
            priceNoBTW = data['priceNoBTW']
        elif data['priceBTW'] != '' and data['priceNoBTW'] == '':
            priceBTW = float(data['priceBTW'])
            priceNoBTW = priceBTW * 0.79
        elif data['priceBTW'] == '' and data['priceNoBTW'] != '':
            priceNoBTW = float(data['priceNoBTW'])
            priceBTW = priceNoBTW * 1.21

        product = Product(title=data['title'],
                    barcode=data['barcode'],
                    priceBTW=priceBTW,
                    priceNoBTW=priceNoBTW,
                    description=data['description'],
                    url=data['url'],
                    notes=data['notes'],
                    manufacturer_id=manufacturer.id,
                    category_id=category.id,
                    vendor_id=vendor.id,
                    quantity_total=data['quantity'],
                    quantity_unavailable=data['quantity_unavailable'],
                    quantity_borrowed='0',
                    )

        db.session.add(product)
        db.session.commit()

        return {
            'success': True
        }

@api.route('/check-name', methods=['POST'])
class CheckName(Resource):
    def post(self):
        data = request.get_json()
        name = data['name']
        product = Product.query.filter_by(title=name).first()

        if product:
            return {
                'message': f'Product name already exists',
                'success': False
            }

        return {
            'message': f'Product name available',
            'success': True
        }

@api.route('/update-product', methods=['POST'])
class UpdateProduct(Resource):
    def post(self):
        data = request.get_json()
        barcode = data['barcode']

        # Get product by barcode
        product = Product.query.filter_by(barcode=barcode).first()

        # Update product
        current_quantity = product.quantity_total
        current_quantity_unavailable = product.quantity_unavailable

        product.quantity_total = int(data['quantity']) + current_quantity
        product.quantity_unavailable = int(data['quantity_unavailable']) + current_quantity_unavailable

        db.session.commit()

        return {
            'success': True
        }

@api.route('/edit-product', methods=['GET', 'POST'])
class EditProduct(Resource):
    def post(self):
        # data = request.form.to_dict(flat=True)
        data = request.get_json()
        print("DATA: ", data)
        values = data['data']

        # Get product by id
        product = Product.query.filter_by(id=data['id']).first()

        product.title = values['title']
        product.barcode = values['barcode']
        product.priceBTW = values['priceBTW']
        product.priceNoBTW = values['priceNoBTW']
        product.description = values['description']
        product.url = values['url']
        product.notes = values['notes']
        product.quantity_total = values['quantity']
        product.quantity_unavailable = values['quantity_unavailable']
        product.manufacturer_id = values['manufacturer']
        product.category_id = values['category']
        product.vendor_id = values['vendor']


        print("Updaten ----------------------------------------------")
        # Commit to database
        db.session.commit()

        return {
            'message': f'Product updated',
            'success': True
        }, 200

@api.route('/delete-product', methods=['POST'])
class DeleteProduct(Resource):
    def post(self):
        data = request.get_json()
        product = Product.query.filter_by(id=data['id']).first()
        if product:
            try:
                db.session.delete(product)
                db.session.commit()
                return {
                'message': f'Product deleted',
                'success': True
                }, 200
            except AssertionError:
                return {
                'message': f'Product could not be deleted. This might be because the product is currently being borrowed.',
                'success': False
                }, 200

        else:
            return {
            'message': f'Product Not Found',
            'success': False
            }, 200

@api.route('/delete-order', methods=['POST'])
class DeleteOrder(Resource):
    def post(self):
        data = request.get_json()
        order = Order.query.filter_by(id=data['id']).first()
        if order:
            if order.user_id == data['user_id'] or data['role'] == 'admin':
                try:
                    db.session.delete(order)
                    db.session.commit()
                    return {
                    'message': f'Order deleted',
                    'success': True
                    }, 200
                except AssertionError:
                    return {
                    'message': f'Order could not be deleted.',
                    'success': False
                    }, 200
            else:
                return {
                'message': f'No Permission to delete this order',
                'success': False
                }, 200
        else:
            return {
            'message': f'Order Not Found',
            'success': False
            }, 200

@api.route('/delete-user', methods=['POST'])
class DeleteUser(Resource):
    def post(self):
        data = request.get_json()
        user = Users.query.filter_by(id=data['id']).first()
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                return {
                'message': f'User deleted',
                'success': True
                }, 200
            except AssertionError:
                return {
                'message': f'User could not be deleted. This might be because the user is currently borrowing something.',
                'success': False
                }, 200

        else:
            return {
            'message': f'User Not Found',
            'success': False
            }, 200

@api.route('/get-options')
class GetOptions(Resource):
    def get(self):
        # Get all manufacturers, categories, and vendors
        manufacturers = [manufacturer.manufacturer_name for manufacturer in Manufacturer.query.all()]
        categories = [category.category_name for category in ProductCategory.query.all()]
        vendors = [vendor.vendor_name for vendor in Vendor.query.all()]

        # sort alphabetically
        manufacturers.sort()
        categories.sort()
        vendors.sort()

        return {
            'success': True,
            'manufacturers': manufacturers,
            'categories': categories,
            'vendors': vendors
        }

@api.route('/orders/add_to_cart', methods=['POST'])
class AddToCart(Resource):
    def post(self):
        data = request.get_json()
        item = Product.query.filter(Product.title.contains(data['item'])).first()
        if item:
            data['id'] = item.id
        cart = session['cart']
        cart.append(data)
        session['cart'] = cart
        return {
            'success': True
        }, 200

@api.route('/orders/update_ordered', methods=['POST'])
class UpdateOrder(Resource):
    def post(self):
        data = request.get_json()
        item = Ordered.query.filter(Ordered.id == data['item_id']).first()
        if item:
            # Dropdown menus
            manufacturer_name = data['manufacturer']
            if manufacturer_name != "Select Manufacturer...":
                manufacturer = Manufacturer.query.filter_by(manufacturer_name=manufacturer_name).first()
                if not manufacturer:
                    manufacturer = Manufacturer(manufacturer_name=manufacturer_name)
                    db.session.add(manufacturer)


            category_name = data['category']
            if category_name != "Select Category...":
                category = ProductCategory.query.filter_by(category_name=category_name).first()
                if not category:
                    category = ProductCategory(category_name=category_name)
                    db.session.add(category)


            vendor_name = data['vendor']
            if vendor_name != "Select Vendor...":
                vendor = Vendor.query.filter_by(vendor_name=vendor_name).first()
                if not vendor:
                    vendor = Vendor(vendor_name=vendor_name)
                    db.session.add(vendor)

            db.session.commit()
            if vendor_name != "Select Vendor...":
                item.vendor_id = vendor.id
            if category_name != "Select Category...":
                item.category_id= category.id
            if manufacturer_name != "Select Manufacturer...":
                item.manufacturer_id= manufacturer.id

            item.title=data['title']
            item.price_when_bought=data['price_when_bought'].replace("€", "").strip()
            item.url=data['url']
            item.quantity=data['quantity']
            item.reason=data['reason']
            item.status=data['status']


            db.session.commit()

        else:
            return {
                'message': 'Item not found',
                'success': False
            }


        return {
                'success': True
            }, 200

@api.route('/product/', methods=['GET'])
class ProductRoute(Resource):
    def get(self):
        all_objects = Product.query.all()
        output = [{'id': obj.id, **ProductForm(obj=obj).data} for obj in all_objects]
        return {
                'data': output,
                'success': True
            }, 200

@api.route('/inventory/', methods=['GET'])
class BorrowRoute(Resource):
    def get(self):
        all_objects = Product.query.all()
        output = [{'id': obj.id, **ProductForm(obj=obj).data} for obj in all_objects]
        return {
                'data': output,
                'success': True
            }, 200

@api.route('/borrowed/', methods=['GET'])
class ReturnRoute(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        all_objects = Borrowed.query.filter_by(user_id=user_id)
        output = [{**BorrowForm(obj=obj).data} for obj in all_objects]
        print(output)
        return {
                'data': output,
                'success': True
            }, 200

@api.route('/manufacturer/', methods=['GET'])
class ManufacturerRoute(Resource):
    def get(self):
        all_objects = Manufacturer.query.all()
        output = [{'id': obj.id, **ManufacturerForm(obj=obj).data} for obj in all_objects]
        return {
                'data': output,
                'success': True
            }, 200

@api.route('/ordered/', methods=['GET'])
class OrderedRoute(Resource):
    def get(self):
        all_objects = Ordered.query.all()
        output = [{'id': obj.id, **OrderedForm(obj=obj).data} for obj in all_objects]
        return {
                'data': output,
                'success': True
            }, 200

@api.route('/vendor/', methods=['GET'])
class VendorRoute(Resource):
    def get(self):
        all_objects = Vendor.query.all()
        output = [{'id': obj.id, **VendorForm(obj=obj).data} for obj in all_objects]
        return {
                'data': output,
                'success': True
            }, 200

@api.route('/home/', methods=['GET'])
class ProductRoute(Resource):
    def get(self):
        all_objects = Product.query.all()
        output = [{'id': obj.id, **ProductForm(obj=obj).data} for obj in all_objects]
        return {
                'data': output,
                'success': True
            }, 200