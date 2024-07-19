from sqlmodel import SQLModel

class ServicesBase(SQLModel):
    service_name : str
    price : float
    duration : int

class BookingBase(SQLModel):
    total_price : float

class BookingCreate(BookingBase):
    pass