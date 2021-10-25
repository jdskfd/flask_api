from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import ForeignKey

Base = declarative_base()
class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key = True)
    name = Column(String(25), nullable = False)
    price = Column(Integer, nullable = False)
    img = Column(String(255), nullable = False)
    description = Column(String(255), nullable = False)

    def __init__(self, name, price, img, description):
        self.name = name
        self.price = price
        self.img = img
        self.description = description
    
    def list_to_json(self):
        return {
        'id':self.id,
        'name':self.name,
        'price':self.price,
        'img':self.img
        }
    
    def detail_to_json(self):
        return {
        'id':self.id,
        'name':self.name,
        'price':self.price,
        'img':self.img,
        'description':self.description
        }
    def __repr__(self):
        return "<Products('%s','%s','%s','%s')>" % (self.id, self.name, self.price, self.description)

class Orders(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key = True)
    products_id = Column(Integer, ForeignKey('products.id'))
    order_uuid = Column(String(50), nullable = False)
    amount = Column(Integer, nullable = False)

    products = relationship("Products", backref=backref('order', order_by = id))

    def __init__(self, products_id, order_uuid, amount):
        self.products_id = products_id
        self.order_uuid = order_uuid
        self.amount = amount
    
    def order_to_json(self, products_name):
        return {
            'id':self.id,
            'products_id':self.products_id,
            'order_uuid':self.order_uuid,
            'amout':self.amount,
            'products_name':products_name
        }