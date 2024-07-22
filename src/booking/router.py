from datetime import datetime
from .schemas import BookingBase, BookingCreate, BookingRead, BookingState, ServicesCreate
from .constants import TimeScheduleObject, TimeSchedule
from fastapi import APIRouter, Depends, HTTPException, status
from src.models import Booking, Pets, Services, Users, PetsBookingsAssociation
from src.database import get_session
from sqlmodel import Session, select
from typing import List, Optional, Annotated

booking_router = APIRouter(prefix="/booking", tags=["booking"])

@booking_router.post("/")
async def add_booking(
    booking : BookingCreate,
    db_session : Session = Depends(get_session)
    ) -> BookingRead:
    service = db_session.exec(select(Services).where(Services.service_id == booking.service_id)).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    customer = db_session.exec(select(Users).where(Users.id == booking.customer_id)).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    # automatically set the price based on the service
    formatted_schedule_datetime = datetime.combine(booking.reserved_day, booking.reserved_time)
    booking_db = Booking(
        status=booking.status,
        total_price=service.price,
        customer_id=booking.customer_id,
        service_id=booking.service_id,
        reserved_date=formatted_schedule_datetime
    )
    db_session.add(booking_db)
    db_session.commit()
    db_session.refresh(booking_db)
    for pets in booking.booking_items_link:
        pets_db = db_session.exec(select(Pets).where(Pets.pet_id == pets.pet_id)).first()
        if not pets_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
        link = PetsBookingsAssociation(
            pet_id=pets.pet_id, 
            booking_id=booking_db.booking_id
        )
        print(pets)
        db_session.add(link)
    db_session.add(booking_db)
    db_session.commit()
    db_session.refresh(booking_db)
    return booking_db

# get all the bookings for that user ? or can be filtered as a query parameter

# ==== Admin-specific access routes ==== #

@booking_router.post('/services')
async def add_service(
    service : ServicesCreate,
    db_session : Session = Depends(get_session)
    ) -> Services:
    service_data = db_session.exec(select(Services).where(Services.service_name == service.service_name)).first()
    if service_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service already exists")
    service_data = Services(
        service_name=service.service_name,
        price=service.price,
        duration=service.duration
    )
    db_session.add(service_data)
    db_session.commit()
    db_session.refresh(service_data)
    return service_data

# TODO: update booking status - if done / cancelled / rescheduled / placed

# TODO: delete booking if the booking is cancelled, completed, or pending

# TODO: when the booking status is updated it will notify the basic users
# through webhooks 

# TODO: get all the booking depending on range 
# this day / this week / this month