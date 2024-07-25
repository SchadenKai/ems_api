from sqlmodel import SQLModel
from pydantic import Field, field_validator
from typing import Optional

class ProductsBase(SQLModel):
    product_name : str
    price : float
    stock : int
    description : str
    photo_url : str
    
class ProductsCreate(ProductsBase):
    photo_url : Optional[str] = None
    @field_validator("product_name", mode="before")
    def lower_case_name(cls, value : str) -> str:
        return value.lower()

class ProductsUpdate(ProductsBase):
    product_name : Optional[str] = None
    price : Optional[float] = None
    stock : Optional[int] = None
    description : Optional[str] = None
    photo_url : Optional[str] = None
    @field_validator("product_name", mode="before")
    def lower_case_name(cls, value : str) -> str:
        return value.lower()

class ProductsRead(ProductsBase):
    product_id : int
    stock : int
    last_updated : str
    description : str
    photo_url : str