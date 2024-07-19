from .schemas import UsersCreate, UsersUpdate, Roles
from src.models import Users, Pets
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select
from src.database import get_session
from typing import Annotated

users_router = APIRouter(prefix='/users', tags=['Users'])

@users_router.get('/{id}')
async def get_user_profile(
    id : int,
    db_session: Session = Depends(get_session)
) -> Users :
    statement = select(Users).where(Users.id == id)
    result : Users | None = db_session.exec(statement).one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return result

# ==== User-specific access routes ==== #

@users_router.post('/')
async def create_user(
    req : UsersCreate,
    db_session: Session = Depends(get_session)
) -> Users:
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

@users_router.put('/{id}')
async def update_user(
    id : int,
    req : UsersUpdate,
    db_session: Session = Depends(get_session)
) -> Users :
    statement = select(Users).where(Users.id == id)
    user = db_session.exec(statement).one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if req.full_name:
        user.full_name = req.full_name
    if req.role:
        user.role = req.role
    if req.email:
        user.email = req.email
    if req.password:
        user.password = req.password
    if req.address:
        user.address = req.address
    if req.phone_number:
        user.phone_number = req.phone_number
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

@users_router.delete('/{id}')
async def delete_user(
    id : int,
    db_session: Session = Depends(get_session)
) -> Users :
    statement = select(Users).where(Users.id == id)
    user = db_session.exec(statement).one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_session.delete(user)
    db_session.commit()
    return {
        "message": f"User {id} deleted successfully",
        "status": status.HTTP_200_OK
    }

# ==== Admin-specific access routes ==== #

@users_router.get('/')
async def get_all_users(
    role : Roles | None = None,
    db_session: Session = Depends(get_session)
) -> list[Users] :
    statement = select(Users).where(Users.role == role) if role is not None else select(Users)
    result : list[Users] = db_session.exec(statement).all()
    return result