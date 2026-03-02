from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="Monitoring Backend API"
    # version="0.1.0"
)

app.include_router(api_router, prefix="/api/v1")

# @app.get("/")
# def root():
#     return {"message": "API is running"}

# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}