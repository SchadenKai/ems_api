import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from .database import get_sqlalchemy_engine, warm_up_connections
from .products.routes import products_router
from .users.routes import users_router
from .config import APP_HOST, APP_PORT

__version__ = os.environ.get("API_VERSION", "0.1")

@asynccontextmanager
async def lifespan(app : FastAPI) -> AsyncGenerator:
    # add authentication / validation 
    # await warm_up_connections()
    print(f"Starting enMedD CHP Backend version {__version__} on http://{APP_HOST}:{str(APP_PORT)}/")
    yield

app = FastAPI(
        title='Bath & Bark EMS API', version=__version__, lifespan=lifespan
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the list of allowed origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)
app.include_router(users_router)