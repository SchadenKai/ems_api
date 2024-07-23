from datetime import datetime
from fastapi import HTTPException, status
from pydantic import ConfigDict, field_validator
from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional, Annotated

class OrderState(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

# Following this pattern to make specific attributes excluded in FastAPI OpenAPI documentation
# https://github.com/tiangolo/fastapi/issues/1378#issuecomment-907021855
class OrderBase(SQLModel):
    class Config:
        underscore_attrs_are_private = True
    status : OrderState | None = Field(default=OrderState.PENDING)
    quantity : Annotated[int, Field(gt=0)] 
    total_price : Annotated[float, Field(gt=0)]

class OrderProductAssociationBase(SQLModel):
    product_id : int
    quantity : int

# only used for validating the request body
class OrdersCreate(OrderBase):
    quantity : int
    total_price : float
    customer_id  : int
    product_items_link : list[OrderProductAssociationBase]
    order_date : None | datetime = datetime.now()
    
    @field_validator("status", mode="before")
    def validate_status(cls, v : OrderState):
        if v != OrderState.PENDING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status must be pending")
    # @field_validator("quantity", mode="before")
    # def validate_quantity(cls, v : int):
    #     if v < 1:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be greater than 0")
    # @field_validator("total_price", mode="before")
    # def validate_total_price(cls, v : float):
    #     if v < 0:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Total price must be greater than 0")
    # @field_validator("total_price", mode="after")
    # def validate_total_price(cls, v : float):   
    #     if v != sum([item.total_price for item in cls.order_items]):
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Total price must be equal to the sum of the total price of the order items")

class OrderUpdate(OrderBase):
    status : Optional[OrderState] = None
    quantity : Annotated[int, Field(gt=0)] | None = None
    total_price : Optional[float] = None
    product_items_link : Optional[list[OrderProductAssociationBase]] = None

class OrderRead(OrderBase):
    order_id : int
    product_items_link : list[OrderProductAssociationBase] | None = None
    order_date : datetime 
