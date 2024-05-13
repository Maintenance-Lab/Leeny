import json

from apps.api import blueprint
from apps.api.forms import *
from apps.authentication.decorators import token_required
from apps.authentication.models import Users
from apps.webapp.models import *
from apps.webapp.forms import *
from flask import request, jsonify, Response, session, flash
from flask_restx import Api, Resource
from werkzeug.datastructures import MultiDict
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta


api = Api(blueprint)

# TODO: DELETE and PUT have to be implemented
# TODO: Implement a user permission system to not allow everyone to access user info
@api.route('/test/', methods=['GET'])
class TestRoute(Resource):
    def get(self):
        return {
                'data': 'Hello World',
                'success': True
            }, 200


@api.route('/barcode-scanning', methods=['POST'])
class BarcodeScanningRoute(Resource):
    def post(self):
        # Get the barcode data from the request
        data = request.get_json()
        barcode = data['barcode']

        # Process the barcode data to generate different data
        updated_string = f"Hello from Flask! You scanned barcode: {barcode}"

        return {
            'data': updated_string,
            'success': True
        }, 200


@api.route('/borrow2', methods=['POST'])
class Borrow2(Resource):
    def post(self):
        print("Session Contents:", session)
        data = request.get_json()['addedBarcodes']

        print("DATA", data)

        for items in data.items():
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
                # user_id = 22
                borrow = Borrowed(user_id=user_id,
                                  product_id=product.id,
                                  quantity=quantity,
                                  estimated_return_date=int(datetime.now().timestamp() + 604800)
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



# HET PROBLEEM: USER ID FROM SESSION IS 1. DEZE HEEFT AL MEERDERE BORROWED ITEMS
# DUS ALS EEN USER HETZELFDE WIL LENEN MOET JE HET OPTELLEN WANT DUBBEL TOEVOEGEN MAG NIET

# @api.route('/borrow2', methods=['POST'])
# class Borrow2(Resource):
#     def post(self):
#         print("Session Contents:", session)
#         data = request.get_json()['addedBarcodes']

#         print("DATA", data)

#         try:
#             for barcode, quantity in data.items():
#                 print("barcode: ", barcode, "quantity: ", quantity)

#                 # If barcode is an int
#                 if barcode.isdigit():
#                     print("Barcode is an int")
#                     # Add 1 to quantity borrowed
#                     product = Product.query.filter_by(barcode=barcode).first()
#                     if product:
#                         product.quantity_borrowed += quantity

#                         # Add borrow entry to borrowed table
#                         user_id = session['_user_id']
#                         # user_id = 22
#                         borrow = Borrowed(user_id=user_id,
#                                           product_id=product.id,
#                                           quantity=quantity,
#                                           estimated_return_date=int(datetime.now().timestamp() + 604800)
#                                           )
#                         print("ADD TO TABLE: ", borrow)

#                         # Check if the user already has a borrowed item with the same product_id
#                         existing_borrow = Borrowed.query.filter_by(user_id=user_id, product_id=product.id).first()
#                         if existing_borrow:
#                             existing_borrow.quantity += quantity
#                             print("Existing borrow found. Quantity updated.")
#                         else:
#                             db.session.add(borrow)
#                             print("New borrow added to table.")

#                     else:
#                         print(f"Product with barcode {barcode} not found.")
#                 else:
#                     print("Barcode is not an int.")

#             # Save changes to database
#             print("COMMITTING CHANGES -------------------------------")
#             db.session.commit()
#             print("Changes committed successfully")
#         except Exception as e:
#             print("Error:", e)
#             db.session.rollback()


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


@api.route('/borrow_rfid', methods=['POST'])
class Borrow(Resource):
    def post(self):
        # Get rfid data from the request
        data = request.get_json()
        uid = data['uid']

        # Query the database for the product based on barcode
        product = Product.query.filter_by(uid=uid).first()
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

@api.route('/return/', methods=['GET'])
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