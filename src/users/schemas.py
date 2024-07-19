from pydantic import EmailStr, field_validator, ConfigDict
from sqlmodel import SQLModel
from enum import Enum
from typing import Optional

class SQLModel(SQLModel):
    model_config = ConfigDict(use_enum_values=True)

class Roles(Enum):
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
    # this will not be part of the table of users 
    # this is only used to validate the pets data that will be inputted to 
    # the pets table. This is attatched here since pets table are dependent from users table.
    # pets data cannot be initialized on its own since it cannot be created without an owner (or an owner_id since
    # it is a foreign key)

    # required to have a pet
    pets : list["PetsBase"] | None = None

class UsersUpdate(UsersBase):
    full_name: Optional[str] = None
    role: Optional[Roles] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None

class PetTypes(Enum):
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
    async def lower_case_type(cls, value : str) -> str:
        return value.lower()
    
    pet_name : str
    age : int 
    type : PetTypes
    breed : str