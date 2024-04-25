import json

from apps.api import blueprint
from apps.api.forms import *
from apps.authentication.decorators import token_required
from apps.authentication.models import Users
from apps.webapp.models import *
from apps.webapp.forms import *
from flask import request, jsonify, Response
from flask_restx import Api, Resource
from werkzeug.datastructures import MultiDict

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


@api.route('/borrow', methods=['POST'])
class Borrow(Resource):
    def post(self):
        # Get the barcode data from the request
        data = request.get_json()
        barcode = data['barcode']

        # Process the barcode data to generate different data
        updated_string = f"Barcode: {barcode}"

        return {
            'data': updated_string,
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

@api.route('/borrowing/', methods=['GET'])
class BorrowRoute(Resource):
    def get(self):
        all_objects = Product.query.all()
        output = [{'id': obj.id, **ProductForm(obj=obj).data} for obj in all_objects]
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