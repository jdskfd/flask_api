from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from model import Base, Products, Orders
from test_data import test_data
from flask import jsonify
import uuid

meta = MetaData
engine = create_engine("mysql+pymysql://root:12345678@127.0.0.1:3306/DB1")
Session = sessionmaker(engine)
Base.metadata.create_all(engine)

#query method
class api_query(object):
    def list_all_products(self, session):
        temp = []
        for product in session.query(Products).all():
            temp.append(product.list_to_json())
        result = jsonify(objects = temp)
        return result
    
    def list_product_detail(self, session, products_id):
        temp = []
        for product in session.query(Products).filter(Products.id == products_id):
            temp.append(product.detail_to_json())
        result = jsonify(objects = temp)
        return result

    def list_order(self, session, order_uuid):
        temp = []
        for orders in session.query(Orders).join(Products, Products.id == Orders.products_id).filter(Orders.order_uuid == order_uuid):
            temp.append(orders.order_to_json(orders.products.name))
        result = jsonify(objects = temp)
        return result

    def place_order(self, session, order_product_id, order_product_amount):
        if order_product_amount <= 0:
            return False
        for i in session.query(Products).filter(Products.id == order_product_id):
            order_uuid = uuid.uuid4()
            order_uuid = str(order_uuid)
            new_order = Orders(order_product_id, order_uuid, order_product_amount)
            session.add(new_order)
            session.commit()
            return order_uuid
        return False
        
        

#session
def api_session(api_method, products_id = '', order_product_id = 0, order_product_amount = 0, order_uuid = ''):
    session = Session()
    apiQuery = api_query()
    try:
        if api_method == 'home':
            return 'home page'
        elif api_method =='list_all_products':
            result = apiQuery.list_all_products(session)
            return result
        elif api_method =='list_product_detail':
            result = apiQuery.list_product_detail(session, products_id)
            return result
        elif api_method =='list_order':
            result = apiQuery.list_order(session, order_uuid)
            return result
        elif api_method =='place_order':
            result =  apiQuery.place_order(session, order_product_id, order_product_amount)
            return result
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def init_database():
    products1 = Products(test_data["amazon"]["name"],3335,test_data["amazon"]["img"],test_data["amazon"]["descriptions"])
    products2 = Products(test_data["google"]["name"],2751,test_data["google"]["img"],test_data["google"]["descriptions"])
    products3 = Products(test_data["tesla"]["name"],909,test_data["tesla"]["img"],test_data["tesla"]["descriptions"])
    try:
        session = Session()
        session.add_all([products1,products2,products3])
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()