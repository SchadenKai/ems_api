from .schemas import PetsCreate, PetsRead, PetsUpdate, UsersCreate, UsersRead, UsersUpdate, Roles, PetsBase
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
) -> UsersRead :
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
) -> UsersRead:
    try: 
        email_exists = db_session.exec(select(Users).where(Users.email == req.email)).first()
        if email_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
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
                    owner=user,
                    gender=pet.gender
                )
                db_session.add(pet_obj)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@users_router.put('/{id}')
async def update_user_and_addpet(
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
                gender=pet.gender,
                owner_id=user.id
            )
            db_session.add(pet_obj)
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

## update pet 
@users_router.put('/pets/{id}')
async def update_pet(
    id : int,
    req : PetsUpdate,
    db_session: Session = Depends(get_session)
) -> Pets :
    statement = select(Pets).where(Pets.pet_id == id)
    pet = db_session.exec(statement).one_or_none()
    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    
    if req.pet_name:
        pet.pet_name = req.pet_name
    if req.age:
        pet.age = req.age
    if req.type:
        pet.type = req.type
    if req.breed:
        pet.breed = req.breed
    if req.gender:
        pet.gender = req.gender
    db_session.add(pet)
    db_session.commit()
    db_session.refresh(pet)
    return pet

## get all pet of a user
@users_router.get('/{owner_id}/pets')
async def get_user_pets(
    owner_id : int,
    db_session: Session = Depends(get_session)
) -> list[PetsRead] :
    statement = select(Pets).where(Pets.owner_id == owner_id)
    pets = db_session.exec(statement).all()
    if not pets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No pets found")
    return pets

@users_router.delete('/{id}')
async def delete_user(
    id : int,
    db_session: Session = Depends(get_session)
) :
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

## delete pet
@users_router.delete('/pets/{id}')
async def delete_pet(
    id : int,
    db_session: Session = Depends(get_session)
) :
    statement = select(Pets).where(Pets.pet_id == id)
    pet = db_session.exec(statement).one_or_none()
    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    db_session.delete(pet)
    db_session.commit()
    return {
        "message": f"Pet {id} deleted successfully",
        "status": status.HTTP_200_OK
    }

@users_router.post('/pets')
async def create_pet(
    pet : PetsCreate,
    db_session: Session = Depends(get_session)
) -> Pets:
    db_user = db_session.exec(select(Users).where(Users.id == pet.owner_id)).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for db_pet in db_user.pets:
        if pet.pet_name == db_pet.pet_name and pet.age == db_pet.age and pet.type == db_pet.type and pet.gender == db_pet.gender:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pet already exists")
    pet = Pets(
        pet_name=pet.pet_name,
        age=pet.age,
        type=pet.type,
        breed=pet.breed,
        gender=pet.gender,
        owner_id=pet.owner_id
    )
    db_session.add(pet)
    db_session.commit()
    db_session.refresh(pet)
    return pet

# ==== Admin-specific access routes ==== #

@users_router.get('')
async def get_all_users(
    role : Roles | None = None,
    db_session: Session = Depends(get_session)
) -> list[UsersRead] :
    statement = select(Users).where(Users.role == role) if role is not None else select(Users)
    db_results = db_session.exec(statement).all()
    if not db_results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
          
    return db_results