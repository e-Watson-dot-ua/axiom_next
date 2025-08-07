from fastapi import APIRouter

from app.api.v1 import divisions

api_router = APIRouter()

# Include division routes
api_router.include_router(divisions.router, prefix="/divisions")

# Add other routers as you create them
# api_router.include_router(users.router, prefix="/users")
# api_router.include_router(orders.router, prefix="/orders")
# api_router.include_router(auth.router, prefix="/auth")
