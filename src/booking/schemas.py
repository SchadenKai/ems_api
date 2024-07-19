from fastapi import HTTPException, status
from pydantic import ConfigDict, field_validator
from sqlmodel import SQLModel, Field
from enum import Enum

class SQLModelBase(SQLModel):
    model_config = ConfigDict(use_enum_values=True)

class BookingState(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class ServicesBase(SQLModel):
    service_name : str
    price : float
    duration : int

class BookingBase(SQLModel):
    status : BookingState | None = Field(default=BookingState.PENDING)
    total_price : float

class BookingCreate(BookingBase):
    @field_validator("status", mode="before")
    def validate_status(cls, v : BookingState):
        if v:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status cannot be set manually")
    