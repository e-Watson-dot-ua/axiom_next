from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import api_router
from app.services.division import (
    DivisionNotFoundError,
    DivisionCodeExistsError, 
    ParentNotFoundError,
    CircularReferenceError,
    SelfParentError,
    HasChildrenError,
    DivisionNotDeletedError
)

# Create FastAPI app
app = FastAPI(
    title = "Axiom Next API",
    description = "Military logistics and transfer management system",
    version = "1.0.0"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],  # React dev server
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# Include API routes
app.include_router(api_router, prefix = "/api")

# Global exception handlers for business logic errors
@app.exception_handler(DivisionNotFoundError)
async def division_not_found_handler(request, exc: DivisionNotFoundError):
    return JSONResponse(
        status_code = 404,
        content = {"detail": f"Division with ID {exc.division_id} not found"}
    )

@app.exception_handler(DivisionCodeExistsError)
async def division_code_exists_handler(request, exc: DivisionCodeExistsError):
    return JSONResponse(
        status_code = 400,
        content = {"detail": f"Division with code '{exc.code}' already exists"}
    )

@app.exception_handler(ParentNotFoundError)
async def parent_not_found_handler(request, exc: ParentNotFoundError):
    return JSONResponse(
        status_code = 400,
        content = {"detail": f"Parent division with ID {exc.parent_id} not found"}
    )

@app.exception_handler(CircularReferenceError)
async def circular_reference_handler(request, exc: CircularReferenceError):
    return JSONResponse(
        status_code = 400,
        content = {"detail": "Cannot create circular parent-child relationship"}
    )

@app.exception_handler(SelfParentError)
async def self_parent_handler(request, exc: SelfParentError):
    return JSONResponse(
        status_code = 400,
        content = {"detail": "Division cannot be its own parent"}
    )

@app.exception_handler(HasChildrenError)
async def has_children_handler(request, exc: HasChildrenError):
    return JSONResponse(
        status_code = 400,
        content = {"detail": f"Cannot delete division with {exc.children_count} child divisions"}
    )

@app.exception_handler(DivisionNotDeletedError)
async def division_not_deleted_handler(request, exc: DivisionNotDeletedError):
    return JSONResponse(
        status_code = 400,
        content = {"detail": f"Division with ID {exc.division_id} is not deleted"}
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "axiom-next-api"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Axiom Next API is running"}

# API version endpoint
@app.get("/api/v1")
async def api_info():
    return {
        "api": "Axiom Next",
        "version": "1.0.0",
        "description": "Military logistics and transfer management system"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host = "0.0.0.0", 
        port = 8000, 
        reload = True
    )
