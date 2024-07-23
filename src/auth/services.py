from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


protected_routes = [
    "/products",
    "/users",
    "/order",
    "/booking"
]
class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
    async def dispatch(self, request, call_next):
        if any([request.url.path.startswith(route) for route in protected_routes]):
            if request.headers.get("Authorization") is None:
                raise HTTPException(status_code=401, detail="Authorization header is missing")
            else:
                print("Authorization header is present")
                return await call_next(request)
        if request.url.path.startswith("/auth"):
            response = await call_next(request)
            return response

        