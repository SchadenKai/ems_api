from datetime import datetime
from fastapi import HTTPException, status
from pydantic import ConfigDict, field_validator, model_validator
from typing import List, Optional, Annotated
from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import date, time

# from src.users.schemas import PetsRead

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
    class Config:
        underscore_attrs_are_private = True
    status : BookingState | None = None
    total_price : float

class BookingCreate(BookingBase):
    @field_validator("status", mode="before")
    def transform_status_value(cls, v : BookingState):
        if v != BookingState.PENDING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status must be pending")
    @model_validator( mode="before")
    def validate_date(cls, data : "BookingCreate"):
        reserved_day = date(*map(int, data.get("reserved_day").split("-")))
        reserved_time = time(*map(int, data.get("reserved_time").split(":")))
        if datetime.combine(reserved_day, reserved_time) < datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Date must be in the future")
    @field_validator("reserved_time", mode="before")
    def validate_time(cls, reserved_time : str):
        reserved_time = datetime.strptime(reserved_time, "%H:%M:%S")
        if reserved_time.hour < 8 or reserved_time.hour > 16:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Time must be between 8 AM and 4 PM only")
        if reserved_time.minute != 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Time must be in whole hours only")
        if reserved_time.second != 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Time must be in whole hours only")
    customer_id : int
    service_id : int
    booking_items_link : list[PetsBookingsAssociation]
    reserved_day : date
    reserved_time : time

class BookingRead(BookingBase):
    customer_id : int
    service_id : int
    service : ServicesBase
    booking_items_link : list[PetsBookingsAssociation] | None = None
    reserved_date : datetime 

class BookingUpdate(BookingBase):
    status : Optional[BookingState] = None
    _total_price : Optional[float] = None
    _booking_items_link : Optional[list[PetsBookingsAssociation]] = None
    _reserved_date : datetime | None = None
