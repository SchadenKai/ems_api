from datetime import datetime
from fastapi import HTTPException, status
from pydantic import ConfigDict, field_validator
from typing import List, Optional, Annotated
from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import date, time

class SQLModelBase(SQLModel):
    model_config = ConfigDict(use_enum_values=True)

class BookingState(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class PetsBookingsAssociation(SQLModel):
    pet_id : int

class ServicesBase(SQLModel):
    service_name : str
    price : float
    # in hours
    duration : int

class ServicesCreate(ServicesBase):
    @field_validator("service_name", mode="before")
    def transform_service_name(cls, v : str):
        return v.lower()

class BookingBase(SQLModel):
    status : BookingState | None = None
    total_price : float

class BookingCreate(BookingBase):
    @field_validator("status", mode="before")
    def transform_status_value(cls, v : BookingState):
        if v != BookingState.PENDING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status must be pending")
    customer_id : int
    service_id : int
    booking_items_link : list[PetsBookingsAssociation]
    reserved_day : date
    reserved_time : time

class BookingRead(BookingBase):
    customer_id : int
    service_id : int
    booking_items_link : list[PetsBookingsAssociation] | None = None
    reserved_date : datetime 