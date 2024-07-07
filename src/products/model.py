from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'
    
    product_id = Column(Integer, primary_key=True)
    sku = Column(String(100))
    name = Column(String(100), nullable=False)
    brand_id = Column(Integer, ForeignKey('brand.brand_id'))
    price = Column(Numeric)
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.category_id'))
    last_update = Column(DateTime)
    
    # Assuming that there are corresponding Brand and Category classes
    brand = relationship("Brand", back_populates="products")
    category = relationship("Category", back_populates="products")

# Example of other classes that might be related
class Brand(Base):
    __tablename__ = 'brand'
    
    brand_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    products = relationship("Product", back_populates="brand")

class Category(Base):
    __tablename__ = 'category'
    
    category_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    products = relationship("Product", back_populates="category")
