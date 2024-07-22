from src.products.schemas import ProductsBase
from .schemas import OrderBase, OrderState, OrdersCreate

def calculate_price(quantity: int, product: ProductsBase) -> float:
    return quantity * product.price

# def get_order_total_price(product : ProductsBase, ) -> float:
#     return order.quantity * sum([product.price for product in order])