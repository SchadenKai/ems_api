from sqlmodel import SQLModel
from pydantic import Field, field_validator
from typing import Optional

class ProductsBase(SQLModel):
    product_name : str
    price : float
    stock : int
    
class ProductsCreate(ProductsBase):
    @field_validator("product_name", mode="before")
    def lower_case_name(cls, value : str) -> str:
        return value.lower()

class ProductsUpdate(ProductsBase):
    product_name : Optional[str] = None
    price : Optional[float] = None
    stock : Optional[int] = None
    @field_validator("product_name", mode="before")
    def lower_case_name(cls, value : str) -> str:
        return value.lower()

class ProductsRead(ProductsBase):
    product_id : int
    stock : int