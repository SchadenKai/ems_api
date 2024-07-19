from sqlmodel import SQLModel

class OrderBase(SQLModel):
    quantity : int 
    total_price : float

# only used for validating the request body
class OrderCreate(OrderBase):
    pass

class OrderItemBase(SQLModel):
    quantity : int
    total_price : float