from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, ARRAY, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Pet(Base):
    __tablename__ = 'pet'
    
    pet_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_name = Column(String(100), nullable=False)
    age = Column(Integer)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))  # To be added later
    type = Column(String(50))
    breed = Column(String(100))
    
    bookings = relationship("Booking", back_populates="pet")

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(106))
    last_name = Column(String(108))
    email = Column(String(100))
    password = Column(String(168))
    address = Column(String(108))
    phone_number = Column(String(100))

    #relationship to Role table
    roles = relationship("Role", backref="users")  
    bookings = relationship("Booking", back_populates="users")

class Role(Base):
    __tablename__ = 'role'

    role_id = Column(Integer, primary_key=True)
    name = Column(String(100))