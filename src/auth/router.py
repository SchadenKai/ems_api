from fastapi import APIRouter, Depends, HTTPException, status
from src.models import Pets, Users
from src.database import get_session
from sqlmodel import Session, select
from pydantic import EmailStr
from typing import List, Optional, Annotated
from src.users.schemas import UsersBase, UsersCreate, UsersRead, UsersUpdate, Roles
from .schemas import LoginBase
from sqlalchemy.exc import SQLAlchemyError

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register")
async def register(
    req : UsersCreate,
    db_session : Session = Depends(get_session)
    ) -> UsersRead:
    try: 
        user = Users(
            full_name=req.full_name,
            role=req.role,
            email=req.email,
            password=req.password,
            address=req.address,
            phone_number=req.phone_number
            )
        if req.pets:
            for pet in req.pets:
                pet_obj = Pets(
                    pet_name=pet.pet_name,
                    age=pet.age,
                    type=pet.type,
                    breed=pet.breed,
                    owner=user
                )
                db_session.add(pet_obj)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@auth_router.post("/login")
async def login(
    payload : LoginBase,
    db_session : Session = Depends(get_session)
    ) -> UsersRead:
    print(payload.password)
    print(f"datatype : {type(payload.password)}")
    user = db_session.exec(select(Users).where(Users.email == payload.email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.password != payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    return user