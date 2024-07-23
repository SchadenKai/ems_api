from pydantic import EmailStr, Field, field_validator, ConfigDict
from sqlmodel import SQLModel
from enum import Enum
from typing import Optional
import hashlib

from src.booking.schemas import BookingBase
from src.order.schemas import OrderBase

class SQLModel(SQLModel):
    model_config = ConfigDict(use_enum_values=True)

class Roles(str, Enum):
    ADMIN = "admin"
    BASIC = "basic"

class UsersBase(SQLModel):
    full_name : str
    role : Roles
    email : EmailStr
    password : str
    address : str
    phone_number : str

class UsersCreate(UsersBase):
    @field_validator("role", mode="before")
    def lower_case_role(cls, v : str):
        return v.lower()
    @field_validator("full_name", mode="before")
    def capitalize_name(cls, v : str):
        return v.title()
    @field_validator("password", mode="after")
    def hash_password(cls, v : str):
        return hashlib.sha256(v.encode()).hexdigest()
    # this will not be part of the table of users 
    # this is only used to validate the pets data that will be inputted to 
    # the pets table. This is attatched here since pets table are dependent from users table.
    # pets data cannot be initialized on its own since it cannot be created without an owner (or an owner_id since
    # it is a foreign key)

    # required to have a pet
    # creation of pets will be done rather than referencing id's of the pets
    pets : list["PetsBase"] | None = None

class UsersUpdate(UsersBase):
    @field_validator("role", mode="before")
    def lower_case_role(cls, v : str):
        return v.lower()
    @field_validator("full_name", mode="before")
    def capitalize_name(cls, v : str):
        return v.title()
    @field_validator("password", mode="after")
    def hash_password(cls, v : str):
        return hashlib.sha256(v.encode()).hexdigest()
    full_name: Optional[str] = None
    role: Optional[Roles] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    pets : list["PetsBase"] | None = None

class UsersRead(UsersBase):
    @field_validator("role", mode="before")
    def lower_case_role(cls, v : str):
        return v.lower()
    full_name : str
    role : Roles
    email : EmailStr
    address : str
    phone_number : str
    pets : list["PetsBase"] | None = None
    orders : list["OrderBase"] | None = None
    booking : list["BookingBase"] | None = None
    password : str = Field(None, exclude=True)
    id : int | None = None

class PetTypes(str, Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    FISH = "fish"
    PIG = "pig"
    HAMSTER = "hamster"
    HEDGEHOG = "hedgehog"
    OTHERS = "others"

class PetsBase(SQLModel):
    @field_validator("type", mode="before")
    def lower_case_type(cls, value : str) -> str:
        return value.lower()
    pet_name : str
    age : int 
    type : PetTypes
    breed : str

class PetsCreate(PetsBase):
    owner_id : int