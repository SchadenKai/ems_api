from datetime import datetime
from fastapi import HTTPException, status
from pydantic import ConfigDict, field_validator, model_validator
from typing import List, Optional, Annotated
from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import date, time

from src.users.schemas import PetsRead, UsersBase, UsersRead

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

class PetsBookingsAssociationRead(PetsBookingsAssociation):
    pet : "PetsRead"

class ServicesBase(SQLModel):
    service_name : str
    price : float
    # in hours
    duration : int

class ServicesCreate(ServicesBase):
    @field_validator("service_name", mode="before")
    def transform_service_name(cls, v : str):
        return v.lower()
    
class ServicesRead(ServicesBase):
    service_id : int

class ServicesReadAdmin(ServicesBase):
    service_id : int
    booking : list["BookingRead"] | None = None
    
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
    customer_id : int
    service_id : int
    booking_items_link : list[PetsBookingsAssociation]
    reserved_day : date
    reserved_time : time

class BookingRead(BookingBase):
    customer_id : int
    service_id : int
    service : ServicesBase
    booking_items_link : list[PetsBookingsAssociationRead] | None = None
    reserved_date : datetime 
    customer : "UsersBase"

class BookingUpdate(BookingBase):
    status : Optional[BookingState] = None
    total_price : Optional[float] = None
    booking_items_link : Optional[list[PetsBookingsAssociation]] = None
    reserved_date : datetime | None = None
