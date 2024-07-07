from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Order(Base):
    __tablename__ = 'order'

    order_id = Column(Integer, primary_key=True)
    users_id = Column(String, ForeignKey('users.users_id'))
    total_price = Column(String)

    #relationship to users table
    users = relationship("Users", backref="orders")  

class OrderItem(Base):
    __tablename__ = 'order_item'

    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.order_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))
    quantity = Column(Integer)
    price = Column(String)

    #relationship to Order and Product tables
    order = relationship("Order")
    product = relationship("Product")