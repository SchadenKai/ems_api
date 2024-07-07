from fastapi import APIRouter
from products.schema import Products

products_router = APIRouter(prefix='/products')

temp_database = []

# TODO: get all the producst 
@products_router.get('/')
async def get_all_products(count : int = 10) -> list[Products]:
    return temp_database[0 : count]

# TODO: get single product
@products_router.get('/{id}')
async def get_product(id : str) -> Products:
    return {}

# ==== Admin-specific access routes ==== #

# TODO: update a single product

# TODO: delete a single / range of products
@products_router.delete('/{id}')
async def delete_product(id : str):
    return {

    }

# TODO: add new products in the inventory
@products_router.post('/')
async def add_product(req : Products):
    temp_database.append(req)
    return {
        "message" : "sent successfully",
        "data" : temp_database
    }