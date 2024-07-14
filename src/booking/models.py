from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, ARRAY, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Service(Base):
    __tablename__ = 'service'
    
    service_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric, nullable=False)
    
    bookings = relationship("Booking", back_populates="service")

class Booking(Base):
    __tablename__ = 'booking'
    
    booking_id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('service.service_id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))  # To be added later
    date_and_time = Column(DateTime, nullable=False)
    reserved_at = Column(DateTime, nullable=False)
    total_price = Column(Numeric, nullable=False)
    
    service = relationship("Service", back_populates="bookings")
    pet = relationship("Pet", back_populates="bookings")
    users = relationship("Users", back_populates="bookings")