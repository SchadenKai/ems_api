from .schemas import OrderRead, OrdersCreate, OrderUpdate, OrderState
from src.database import get_session
from src.models import Orders, Products, Users, OrderProductAssociation
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlmodel import Session, select, delete
from typing import List, Annotated, Optional
from src.constants import UserType

order_router = APIRouter(prefix='/orders', tags=['Orders'])

# Request cancellation of order 
@order_router.put('/cancel/{order_id}', summary="Request cancellation of order")
async def request_cancellation(
    order_id : int,
    db_session : Session = Depends(get_session)
    ):
    order = db_session.exec(select(Orders).where(Orders.order_id == order_id)).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    order.status = OrderState.CANCELLED
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    return order

@order_router.get('/{order_id}')
async def get_order_by_id(
    order_id : int,
    db_session : Session = Depends(get_session)
    ) -> OrderRead:
    order_db = db_session.exec(select(Orders).where(Orders.order_id == order_id)).one_or_none()
    if not order_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    order_data = OrderRead(
        order_id=order_db.order_id,
        status=order_db.status,
        quantity=order_db.quantity,
        total_price=order_db.total_price,
        customer_id=order_db.customer_id,
        order_date=order_db.order_date,
        product_items_link=[
            # fix this
            OrderProductAssociation(
                product_id=product.product_id,
                quantity=product.quantity
            ) for product in order_db.product_items_link
        ],
    )
    return order_data

# ==== User-specific access routes ==== #

@order_router.post('/')
async def place_order(
    req : OrdersCreate,
    db_session : Session = Depends(get_session)
    ) -> OrderRead:
    # check if the user exists
    temp_memory = []
    user = db_session.exec(select(Users).where(Users.id == req.customer_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    order_data = Orders(
        status=req.status,
        quantity=req.quantity,
        total_price=req.total_price,
        customer_id=req.customer_id,
        order_date=req.order_date
    )
    db_session.add(order_data)
    db_session.commit()
    db_session.refresh(order_data)
    # check if the product exists   
    for product_items in req.product_items_link:
        product = db_session.exec(select(Products).where(Products.product_id == product_items.product_id)).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        temp_memory.append({
            "product_price" : product.price,
            "product_quantity" : product_items.quantity
        })
        link = OrderProductAssociation(
            product_id=product_items.product_id,
            order_id=order_data.order_id,
            quantity=product_items.quantity
        )
        db_session.add(link)
    # replace with calculated total price and quantity from all the products 
    order_data.total_price = sum([item["product_price"] * item["product_quantity"] for item in temp_memory])
    order_data.quantity = sum([item["product_quantity"] for item in temp_memory])
    db_session.add(order_data)
    db_session.commit()
    db_session.refresh(order_data)
    return order_data

@order_router.put('/{order_id}')
async def update_order(
    order_id : int,
    req : OrderUpdate,
    db_session : Session = Depends(get_session)
    ) -> Orders:
    temp_memory = []
    order = db_session.exec(select(Orders).where(Orders.order_id == order_id)).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if req.status:
        order.status = req.status
    if req.quantity:
        order.quantity = req.quantity
    if req.total_price:
        order.total_price = req.total_price
    if req.product_items_link:
        for product_item in req.product_items_link:
            product = db_session.exec(select(Products).where(Products.product_id == product_item.product_id)).first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
            temp_memory.append({
            "product_price" : product.price,
            "product_quantity" : product_item.quantity
            })
            link = OrderProductAssociation(
                order_id=order.order_id,
                product_id=product_item.product_id,
                quantity=product_item.quantity
            )
            if db_session.exec(select(OrderProductAssociation).where(OrderProductAssociation.order_id == order.order_id and OrderProductAssociation.product_id == product_item.product_id)).first():
                db_session.exec(delete(OrderProductAssociation).where(OrderProductAssociation.order_id == order.order_id and OrderProductAssociation.product_id == product_item.product_id))
            db_session.add(link)
        order.total_price = sum([item["product_price"] * item["product_quantity"] for item in temp_memory])
        order.quantity = sum([item["product_quantity"] for item in temp_memory])
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    return order

# ==== Admin-specific access routes ==== #

# update the status from the order 
@order_router.put('/status/{order_id}')
async def update_order_status(
    order_id : int,
    req : OrderUpdate,
    db_session : Session = Depends(get_session)
    ) -> Orders:
    order = db_session.exec(select(Orders).where(Orders.order_id == order_id)).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if req.status == order.status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status must be different")
    order.status = req.status
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    return order

@order_router.get('/')
async def get_all_orders(
    limit : Annotated[int, Query(gt=0, le=100)] | None = None,
    status : Optional[OrderState] = None,
    db_session : Session = Depends(get_session)
    ) -> List[OrderRead]:
    if status:
        orders_db = db_session.exec(select(Orders).where(Orders.status == status)).all()
    else:
        orders_db = db_session.exec(select(Orders)).all() 
    orders = orders_db[:limit] if limit is not None else orders_db
    return orders

# Delete order only if the order status is pending or cancelled
@order_router.delete('/')
async def delete_order(
    # delete multiple orders ex. /orders?list=1,2,3
    list : List[str] = Query(None),
    db_session : Session = Depends(get_session)
    ):
    if list:
        for order_id in list:
            order = db_session.exec(select(Orders).where(Orders.order_id == order_id)).first()
            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
            if order.status == OrderState.CONFIRMED:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order cannot be deleted")
            db_session.delete(order)
        db_session.commit()
        return { "status" : status.HTTP_200_OK, "message" : "Orders deleted successfully" }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No order id provided")