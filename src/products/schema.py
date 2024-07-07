from pydantic import BaseModel
from datetime import datetime

class Categories(BaseModel):
    category_id : int | None
    name : str

class Brand(BaseModel):
    brand_id : int | None
    name : str

class Products(BaseModel):
    product_id : str | None
    sku : str | None 
    name : str
    price : float
    stock : int
    last_update : datetime | None