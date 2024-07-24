from datetime import date, datetime, timedelta
from .schemas import BookingBase, BookingCreate, BookingRead, BookingState, BookingUpdate, ServicesCreate, ServicesRead
from .constants import BookingRange
from fastapi import APIRouter, Depends, HTTPException, Query, status
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

# user-specific get bookings route
@booking_router.get("/user/{user_id}")
async def get_all_bookings(
    user_id : int,
    db_session : Session = Depends(get_session),
    range : Optional[BookingRange] = Query(None)
    ) -> List[BookingRead]:
    if range:
        if range == BookingRange.TODAY:
            booking_data = db_session.exec(select(Booking).where(Booking.customer_id == user_id)).all()
            booking_filtered = [
                booking for booking in booking_data if booking.reserved_date.date() == date.today()
            ]
            return booking_filtered
        elif range == BookingRange.WEEK:
            start_of_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
            end_of_week = start_of_week + timedelta(days=6)
            booking_data = db_session.exec(select(Booking).where(Booking.reserved_date >= start_of_week, Booking.reserved_date <= end_of_week, Booking.customer_id == user_id)).all()
            return booking_data
        elif range == BookingRange.MONTH:
            start_of_month = datetime.now().date().replace(day=1)
            end_of_month = start_of_month + timedelta(days=30)
            booking_data = db_session.exec(select(Booking).where(Booking.reserved_date >= start_of_month, Booking.reserved_date <= end_of_month, Booking.customer_id == user_id)).all()
            return booking_data
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid range")


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

@booking_router.put("/status/{booking_id}")
async def update_booking_status(
    booking_id : int,
    booking : BookingUpdate,
    db_session : Session = Depends(get_session)
    ) -> BookingRead:
    booking_data = db_session.exec(select(Booking).where(Booking.booking_id == booking_id)).first()
    if not booking_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    booking_data.status = booking.status
    db_session.add(booking_data)
    db_session.commit()
    db_session.refresh(booking_data)
    return booking_data

@booking_router.delete("/")
async def delete_booking(
    list : List[str],
    db_session : Session = Depends(get_session)
    ) -> BookingRead:
    for booking_id in list:
        booking_data = db_session.exec(select(Booking).where(Booking.booking_id == booking_id)).first()
        if not booking_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if booking_data.status == BookingState.CONFIRMED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Booking cannot be deleted if it is confirmed")
        db_session.delete(booking_data)
        db_session.commit()
    return {
        "status" : HTTPException(status_code=status.HTTP_200_OK, detail="Booking deleted")
    }

# this day / this week / this month
@booking_router.get("/")
async def get_all_bookings(
    db_session : Session = Depends(get_session),
    range : BookingRange | None = None
    ) -> List[BookingRead]:
    if range:
        if range == BookingRange.TODAY:
            booking_data = db_session.exec(select(Booking)).all()
            booking_filtered = [
                booking for booking in booking_data if booking.reserved_date.date() == date.today()
            ]
            return booking_filtered
        elif range == BookingRange.WEEK:
            start_of_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
            end_of_week = start_of_week + timedelta(days=6)
            booking_data = db_session.exec(select(Booking).where(Booking.reserved_date >= start_of_week, Booking.reserved_date <= end_of_week)).all()
            return booking_data
        elif range == BookingRange.MONTH:
            start_of_month = datetime.now().date().replace(day=1)
            end_of_month = start_of_month + timedelta(days=30)
            booking_data = db_session.exec(select(Booking).where(Booking.reserved_date >= start_of_month, Booking.reserved_date <= end_of_month)).all()
            return booking_data
    else:
        booking_data = db_session.exec(select(Booking)).all()
        return booking_data

## Get all services
@booking_router.get("/services")
async def get_all_services(
    db_session : Session = Depends(get_session)
    ) -> List[ServicesRead]:
    service_data = db_session.exec(select(Services)).all()
    return service_data