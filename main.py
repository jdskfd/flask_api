from flask import Flask, jsonify
from flask_restful import Resource, Api, abort, reqparse
from model import Products, Orders
from test_data import test_data
from connection import init_database, api_session
import json

app = Flask(__name__)
api = Api(app)

#parser
parser = reqparse.RequestParser()
parser.add_argument('order_product_id', type = int, required = True, help = 'Product id is Required.')
parser.add_argument('order_product_amount', type = int, required = True, help = 'Product Amount is Required.')
#route
class Home(Resource):
    def get(self):
        result = api_session('home')
        return result

class ProductsList(Resource):
    def get(self):
        result = api_session('list_all_products')
        return result

class ProductsDetail(Resource):
    def get(self, products_id):
        result = api_session('list_product_detail', products_id)
        return result

class ListOrder(Resource):
    def get(self, order_uuid):
        result = api_session('list_order', order_uuid = order_uuid)
        return result

class PlaceOrder(Resource):    
    def post(self):
        args = parser.parse_args()
        result = api_session('place_order', order_product_id = args['order_product_id'], order_product_amount = args['order_product_amount'])
        if result == False:
            return "Wrong data"
        else:
            result = "Order uuid is: " + result
            return result
    
class InitDatabase(Resource):
    def get(self):
        init_database()
        return "DataBase init."

api.add_resource(Home, '/')
api.add_resource(ProductsList, '/products')
api.add_resource(ProductsDetail, '/products/<string:products_id>')
api.add_resource(PlaceOrder,'/order')
api.add_resource(ListOrder, '/order/<string:order_uuid>')
api.add_resource(InitDatabase, '/init_database')

if __name__ == "__main__":
    app.run()