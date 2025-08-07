from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="Axiom Next API",
    description="Military logistics and transfer management system",
    version="1.0.0"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "axiom-api"}

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
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
