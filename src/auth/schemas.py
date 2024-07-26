from pydantic import EmailStr, field_validator, ConfigDict, BaseModel
import hashlib
from src.booking.schemas import BookingBase
from src.order.schemas import OrderBase
from src.users.schemas import UsersRead, PetsBase


class LoginBase(BaseModel):
    email : EmailStr
    password : str

    @field_validator("email", mode="before")
    def lower_case_email(cls, v : str):
        return v.lower()
    @field_validator("password", mode="after")
    def hash_password(cls, v : str):
        return hashlib.sha256(v.encode()).hexdigest()
    
class LoginRead(BaseModel):
    token : str
    user : UsersRead

class ChangePassword(BaseModel):
    @field_validator("old_password", mode="before")
    def hash_old_password(cls, v : str):
        return hashlib.sha256(v.encode()).hexdigest()
    @field_validator("new_password", mode="after")
    def hash_new_password(cls, v : str):
        return hashlib.sha256(v.encode()).hexdigest()
    old_password : str
    new_password : str