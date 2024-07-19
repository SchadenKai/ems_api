from src.users.schemas import UsersBase, PetsBase
from sqlmodel import Field, Relationship, SQLModel
from src.order.schemas import OrderBase
from src.products.schemas import ProductsBase
from src.booking.schemas import ServicesBase, BookingBase
from datetime import datetime
import pytz

timezone = pytz.timezone("Asia/Manila")

# ---- Link Tables ------

class PetsBookingsAssociation(SQLModel, table=True):
    pet_id : int = Field(foreign_key="pets.pet_id", primary_key=True)
    booking_id : int = Field(foreign_key="booking.booking_id", primary_key=True)

class OrderProductAssociation(SQLModel, table=True):
    order_id : int = Field(foreign_key="pets.order_id", primary_key=True)
    product_id : int = Field(foreign_key="booking.product_id", primary_key=True)

# ----- Users and Pets Models -----

class Users(UsersBase, table=True):
    id : int | None = Field(default=None, primary_key=True)

    pets : list["Pets"] = Relationship(sa_relationship_kwargs={"cascade" : "all, delete"}, back_populates="owner")
    orders : list["Orders"] = Relationship(sa_relationship_kwargs={"cascade" : "all, delete"}, back_populates="customer")
    booking : list["Booking"] = Relationship(sa_relationship_kwargs={"cascade" : "all, delete"}, back_populates="customer")

class Pets(PetsBase, table=True):
    pet_id : int | None = Field(default=None, primary_key=True)
    owner_id : int = Field(foreign_key="users.id")
    
    booking : list["Booking"] = Relationship(sa_relationship_kwargs={"cascade" : "all, delete"}, back_populates="pets", link_model=PetsBookingsAssociation)
    owner : "Users" = Relationship(back_populates="pets")

# ----- Products Models -----

class Products(ProductsBase, table=True):
    product_id : int | None = Field(default=None, primary_key=True)
    last_updated : datetime | None = Field(default=datetime.now(timezone)) 

    order_items : list["Orders"] = Relationship(sa_relationship_kwargs={"cascade" : "all, delete"}, back_populates="product_items", link_model=OrderProductAssociation)


# ----- Booking and Services Models -----

class Services(ServicesBase, table=True):
    service_id : int | None = Field(default=None, primary_key=True)

    booking : list["Booking"] = Relationship(sa_relationship_kwargs={"cascade" : "all, delete"}, back_populates="service")

class Booking(BookingBase, table=True):
    booking_id : int | None = Field(default=None, primary_key=True)
    reserved_date : datetime | None = Field(default=datetime.now(timezone))
    service_id : int = Field(foreign_key="services.service_id")
    customer_id : int = Field(foreign_key="users.id")
    
    pets : list["Pets"] = Relationship(sa_relationship_kwargs={"cascade" : "all, delete"}, back_populates="booking", link_model=PetsBookingsAssociation)
    customer : "Users" = Relationship(back_populates="booking")
    service : "Services" = Relationship(back_populates="booking")


# ----- Order and OrderItems Models -----

class Orders(OrderBase, table=True):
    order_id : int | None = Field(default=None, primary_key=True)
    order_date : datetime | None = Field(default=datetime.now(timezone)) 
    customer_id : int = Field(default=None, foreign_key="users.id")
    
    customer : "Users" = Relationship(back_populates="orders")
    product_items : list["Products"] = Relationship(sa_relationship_kwargs={"cascade" : "all, delete"}, back_populates="order_items", link_model=OrderProductAssociation)

