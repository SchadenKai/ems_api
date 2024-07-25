from fastapi import APIRouter, Depends, HTTPException, Query, status
from .schemas import ProductsBase, ProductsCreate, ProductsUpdate
from sqlmodel import Session, select, delete
from src.database import get_session
from sqlalchemy.exc import SQLAlchemyError
from src.models import Products
from datetime import datetime
from typing import Annotated

products_router = APIRouter(prefix='/products', tags=["Products"])


@products_router.get('/{id}')
async def get_product(
    id : int,
    db_session : Session = Depends(get_session)
    ) -> Products:
    product_data = db_session.get(Products, id)
    if product_data is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_data

@products_router.get('/')
async def get_all_products(
    limit : Annotated[int, Query(le=100, alias='limit')] = 100,
    db_session : Session = Depends(get_session)
    ) -> list[Products]:
    statement = select(Products).limit(limit)
    products_data = db_session.exec(statement).all()
    return products_data

# ==== Admin-specific access routes ==== #

@products_router.put('/{id}')
async def update_product(
    id : int, 
    req : ProductsUpdate,
    db_session : Session = Depends(get_session)
    ):
    statement = select(Products).where(Products.product_id == id)
    product_data : Products | None = db_session.exec(statement).one_or_none()
    if product_data is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if req.product_name:
        product_data.product_name = req.product_name
    if req.price:
        product_data.price = req.price
    if req.stock:
        product_data.stock = req.stock
    if req.description:
        product_data.description = req.description
    product_data.last_updated = datetime.now()
    db_session.add(product_data)
    db_session.commit()
    db_session.refresh(product_data)
    return product_data

@products_router.delete('/{id}')
async def delete_product(
    id : int,
    db_session : Session = Depends(get_session)
    ):
    statement = select(Products).where(Products.product_id == id)
    product_result = db_session.exec(statement).one_or_none()
    if product_result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_session.delete(product_result)
    db_session.commit()
    return {
        "message": f"Product with ID {id} has been deleted",
        "status": status.HTTP_200_OK
    }

@products_router.post('/')
async def add_product(
    req : ProductsCreate,
    db_session : Session = Depends(get_session)
    ) -> Products:
    try:
        new_product = Products(
            product_name=req.product_name,
            price=req.price,
            stock=req.stock,
            description=req.description
        )
        if req.photo_url:
            new_product.photo_url = req.photo_url
        db_session.add(new_product)
        db_session.commit()
        db_session.refresh(new_product)
        return new_product
    except SQLAlchemyError as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail="Error adding product to the database")
