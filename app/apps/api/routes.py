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
from apps.scripts.email_verif import send_email


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



@api.route('/borrow', methods=['POST'])
class Borrow(Resource):
    def post(self):
        # Get the barcode data from the request
        data = request.get_json()
        barcode = data['barcode']
        print("BARCODE: ", barcode)

        # Query the database for the product based on barcode
        product = Product.query.filter_by(barcode=barcode).first()
        print("PRODUCT: ", product)

        if product is not None:
            title = product.title
            quantity_total = product.quantity_total
            quantity_unavailable = product.quantity_unavailable
            quantity_borrowed = product.quantity_borrowed

            quantity = quantity_total - quantity_unavailable - quantity_borrowed

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
                print("Barcode is an int")
                # Add 1 to quantity borrowed
                product = Product.query.filter_by(barcode=barcode).first()
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


        # Send email to users
        user_id = session['_user_id']
        user = Users.query.filter_by(id=user_id).first()
        email = user.email

        timestamp = datetime.fromtimestamp(int(session['estimated_return_date'])).strftime('%d-%m-%Y')
        html = render_template('app/email_overview.html', timestamp=timestamp)
        send_email(email, "Borrow overview", html)



@api.route('/return', methods=['POST'])
class Return(Resource):
    def post(self):
        # Get the barcode data from the request
        data = request.get_json()
        barcode = data['barcode']

        # Query the database for the product based on barcode
        product = Product.query.filter_by(barcode=barcode).first()

        if product is not None:
            title = product.title

            # quantity for borrowed from user
            user_id = session['_user_id']
            borrow = Borrowed.query.filter_by(user_id=user_id, product_id=product.id).first()
            quantity = borrow.quantity

            if borrow is not None:
                # Product found
                output = {
                    'barcode': barcode,
                    'name': title,
                    'quantity': quantity,
                    'message': f'Product found',
                    'success': True
                }
            else:
                # Product not found
                output = {
                    'barcode': barcode,
                    'message': f'Product not found',
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


@api.route('/return2', methods=['POST'])
class Return2(Resource):
    def post(self):
        print("IN RETURN 2")
        print("Session Contents:", session)
        return_data = request.get_json()['addedBarcodes']
        session['return_data'] = return_data

        addedProducts = {}

        for items in return_data.items():
            barcode = items[0]
            quantity = items[1]

            if barcode != 'null':
                # get product name
                product = Product.query.filter_by(barcode=barcode).first()
                product_name = product.title
                addedProducts[product_name] = quantity

        session["addedProducts"] = addedProducts


@api.route('/return-confirm', methods=['POST'])
class ReturnConfirm(Resource):
    def post(self):
        return_data = session['return_data']

        for items in return_data.items():
            print("barcode: ", items[0], "quantity: ", items[1])
            barcode = items[0]
            quantity = items[1]

            # If barcode is an int
            if barcode != 'null':
                print("Barcode is an int")
                # Subtract from quantity borrowed
                product = Product.query.filter_by(barcode=barcode).first()
                product.quantity_borrowed -= quantity

                # Change/remove borrow entry from borrowed table
                user_id = session['_user_id']
                borrow = Borrowed.query.filter_by(user_id=user_id, product_id=product.id).first()
                borrow.quantity -= quantity

                print("New borrowed quantity: ", borrow.quantity)
                print("Product quantity borrowed: ", product.quantity_borrowed)

                if borrow.quantity <= 0:
                    db.session.delete(borrow)
                    print("Borrow entry removed from table.")
                else:
                    print("Quantity updated in borrow table.")

        # Save changes to database
        print("COMMITING CHANGES -------------------------------")
        db.session.commit()


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

        product = Product(title=data['title'],
                            barcode=data['barcode'],
                            price_when_bought=data['price'],
                            description=data['description'],
                            url=data['url'],
                            notes=data['notes'],
                            created_at_ts=datetime.now(),
                            manufacturer_id=data['manufacturer'],
                            category_id=data['category'],
                            vendor_id=data['vendor'],
                            quantity_total=data['quantity'],
                            quantity_unavailable=data['quantity_unavailable'],
                            quantity_borrowed='0',
                            )

        db.session.add(product)
        db.session.commit()

        return {
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
        product.price_when_bought = values['price']
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
        print(session['cart'])
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
        print(output)
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

@api.route('/item/<int:id>', methods=['GET'])

@api.route('/item/<int:id>', methods=['GET'])
class ItemRoute(Resource):
    def get(self, id):
        all_objects = Product.query.filter(Product.id == id)
        output = [{'id': obj.id, **ProductForm(obj=obj).data} for obj in all_objects]
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