from fastapi import HTTPException, status
from pydantic import ConfigDict, field_validator
from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional

class OrderState(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class OrderBase(SQLModel):
    status : OrderState | None = Field(default=OrderState.PENDING)
    quantity : int 
    total_price : float

# only used for validating the request body
class OrderCreate(OrderBase):
    order_items : list["OrderItemBase"]
    @field_validator("status", mode="before")
    def validate_status(cls, v : OrderState):
        if v:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status cannot be set manually")
    
class OrderUpdate(OrderBase):
    status : Optional[OrderState]
    quantity : Optional[int]
    total_price : Optional[float]

class OrderItemBase(SQLModel):
    quantity : int
    total_price : float