from pydantic import EmailStr, field_validator, ConfigDict, BaseModel
import hashlib
# from src.users.schemas import UsersBase


class LoginBase(BaseModel):
    email : EmailStr
    password : str

    @field_validator("email", mode="before")
    def lower_case_email(cls, v : str):
        return v.lower()
    @field_validator("password", mode="after")
    def hash_password(cls, v : str):
        return hashlib.sha256(v.encode()).hexdigest()