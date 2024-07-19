from .schemas import OrdersCreate
from src.database import get_session
from src.models import Orders, Products
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select, delete
from typing import List, Annotated

order_router = APIRouter(prefix='/orders', tags=['Orders'])

# TODO: cancel order / this would send cancellation 
# request to the admin. If the admin agrees, the order will be deleted
# - could be a two way proces from the user to the admin 
# then the admin to the database
# TODO: implement using webhooks

# TODO: get status from the order 
# this can be implemented either through open connection / webhooks / message broker

# ==== User-specific access routes ==== #

# TODO: place the order 
@order_router.post('/')
async def place_order(
    req : OrdersCreate,
    db_session : Session = Depends(get_session)
    ) -> Orders:
    order_data = Orders(
        customer_id=req.customer_id,
        status=req.status,
        quantity=req.quantity,
        total_price=req.total_price,
    )
    for order_item in req.order_items:
        valid_order_item = Products(
        )
        db_session.add(valid_order_item)
    print("acceptedddddd", req)
    db_session.add(order_data)
    db_session.commit()
    db_session.refresh(order_data)
    return order_data

# ==== Admin-specific access routes ==== #

# TODO: update the status from the order 

# TODO: get all the order depending on range in terms of data
