from fastapi import HTTPException, status
from pydantic import ConfigDict, field_validator
from sqlmodel import SQLModel, Field
from src.products.schemas import ProductsBase
from enum import Enum
from typing import Optional, Annotated

class OrderState(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class OrderBase(SQLModel):
    status : OrderState | None = Field(default=OrderState.PENDING)
    quantity : Annotated[int, Field(gt=0)] 
    total_price : Annotated[float, Field(gt=0)]

# only used for validating the request body
class OrdersCreate(OrderBase):
    order_items : list["OrderItemCreate"]
    @field_validator("status", mode="before")
    def validate_status(cls, v : OrderState):
        if v:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status cannot be set manually")
    @field_validator("quantity", mode="before")
    def validate_quantity(cls, v : int):
        if v < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be greater than 0")
    @field_validator("total_price", mode="before")
    def validate_total_price(cls, v : float):
        if v < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Total price must be greater than 0")
    @field_validator("total_price", mode="after")
    def validate_total_price(cls, v : float):   
        if v != sum([item.total_price for item in cls.order_items]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Total price must be equal to the sum of the total price of the order items")

class OrderUpdate(OrderBase):
    status : Optional[OrderState] = None
    quantity : Annotated[int, Field(gt=0)] | None = None
    total_price : Optional[float] = None

class OrderItemBase(SQLModel):
    quantity : Annotated[int, Field(gt=0)]
    total_price : Annotated[float, Field(gt=0)]

class OrderItemCreate(OrderItemBase):
    product : "ProductsBase"
    @field_validator("quantity", mode="before")
    def validate_quantity(cls, v : int):
        if v < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be greater than 0")
    @field_validator("total_price", mode="before")
    def validate_total_price(cls, v : float):
        if v < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Total price must be greater than 0")
    @field_validator("total_price", mode="after")
    def validate_total_price(cls, v : float):   
        if v != cls.product.price * cls.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Total price must be equal to the product price multiplied by the quantity")