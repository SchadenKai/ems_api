from enum import Enum

class UserType(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    MANAGER = "manager" 
