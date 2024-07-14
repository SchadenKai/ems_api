from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'
    
    product_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric)
    stock = Column(Integer)
    last_update = Column(DateTime)

