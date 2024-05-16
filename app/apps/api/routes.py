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
from apps.scripts.email_verif import send_email


api = Api(blueprint)

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
            if barcode.isdigit():
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

        # Send email to user
        user_id = session['_user_id']
        user = Users.query.filter_by(id=user_id).first()
        email = user.email

        session['email_code'] = random.randint(0000, 9999)
        html = render_template('app/borrow-confirm.html')
        send_email(email, "leeny test", html)



@api.route('/authenticate_admin', methods=['POST'])
class AuthenticateAdmin(Resource):
    def post(self):
        data = request.get_json()
        uid = data['uid']

        try:
            user = Users.query.filter_by(uid_1=uid).first()
        except:
            try:
                user = Users.query.filter_by(uid_2=uid).first()
            except:
                try:
                    user = Users.query.filter_by(uid_3=uid).first()
                except:
                    user = None

        if user:
            print("User role: ", user.role)
            if user.role == 'admin':
                return {'authenticated': True, 'role': 'admin'}
            else:
                return {'authenticated': True, 'role': 'student'}
        else:
            return {'authenticated': False}


@api.route('/borrow', methods=['POST'])
class Borrow(Resource):
    def post(self):
        # Get the barcode data from the request
        data = request.get_json()
        barcode = data['barcode']

        # Query the database for the product based on barcode
        product = Product.query.filter_by(barcode=barcode).first()

        if product is not None:
            title = product.title
            quantity_total = product.quantity_total
            quantity_unavailable = product.quantity_unavailable
            quantity_borrowed = product.quantity_borrowed

            quantity = quantity_total - quantity_unavailable - quantity_borrowed

            if quantity <= 0:
                # Product not available
                output = {
                    'barcode': barcode,
                    'name': title,
                    'message': f'Product not available',
                    'success': False
                }

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

        return output, 200


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

            if barcode.isdigit():
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
            if barcode.isdigit():
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


@api.route('/borrow_rfid', methods=['POST'])
class Borrow(Resource):
    def post(self):
        # Get rfid data from the request
        data = request.get_json()
        uid = data['uid']

        # Query the database for the product based on barcode
        product = Product.query.filter_by(item_uid=uid).first()
        title = product.title
        quantity = product.quantity

        if product is not None:
            # Product found
            output = {
                'uid': uid,
                'name': title,
                'quantity': quantity,
                'message': f'Product found',
                'success': True
        }
        else:
            # Product not found
            output = {
                'uid': uid,
                'message': f'Product not found',
                'success': False
        }

        return output, 200


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