from datetime import datetime
import os
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

import yaml

from src.models import Products, Services
from .database import get_session, get_sqlalchemy_engine, warm_up_connections
from .products.routes import products_router
from .users.routes import users_router
from .order.routes import order_router
from .booking.router import booking_router
from .auth.router import auth_router
from .config import APP_HOST, APP_PORT
from .auth.services import AuthMiddleware


__version__ = os.environ.get("API_VERSION", "0.1")

@asynccontextmanager
async def lifespan(app : FastAPI) -> AsyncGenerator:
    # add authentication / validation 
    # await warm_up_connections()
    print(f"Starting Ecommerce Management System version {__version__} on http://{APP_HOST}:{str(APP_PORT)}/")
    yield

app = FastAPI(
        title='Bath & Bark EMS API', version=__version__, lifespan=lifespan
    )

### add middleware for authentication system

app.add_middleware(AuthMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the list of allowed origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)
app.include_router(users_router)
app.include_router(order_router)
app.include_router(booking_router)
app.include_router(auth_router)

# @app.get("/generate_default_data")
# async def generate_default_data_from_yaml(
#     db_session = Depends(get_session)
# ):
#     with open('src\default_data.yml', "r") as file:
#         data = yaml.safe_load(file)
#     # product_data = [
#     #     Products(
#     #     product_name=data.get('product_name'),
#     #     price=data.get('price'),
#     #     stock=data.get('stock'),
#     #     last_updated=datetime.now()
#     #     ) for data in data.get('products')
#     # ]
#     # db_session.add_all(product_data)
#     # db_session.commit()
#     # db_session.refresh(product_data)
#     # print(product_data)
#     services_data = [
#         Services(
#             service_name=data.get('service_name'),
#             price=data.get('price'),
#             duration=data.get('duration')
#         ) for data in data.get('services')
#     ]
#     db_session.add_all(services_data)
#     db_session.commit()
#     db_session.refresh(services_data)
#     print(services_data)
#     return {"message": "Default data generated successfully"}