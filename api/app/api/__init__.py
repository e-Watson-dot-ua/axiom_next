from fastapi import APIRouter

from app.api.v1 import api_router as v1_router

api_router = APIRouter()

# Include V1 API routes
api_router.include_router(v1_router, prefix="/v1")

# Future versions can be added here
# api_router.include_router(v2_router, prefix="/v2")
