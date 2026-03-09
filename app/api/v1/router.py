from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api.deps import get_db
from app.api.v1.endpoints import hosts, items, auth

api_router = APIRouter()

api_router.include_router(
    hosts.router,
    prefix="/hosts",
    tags=["Hosts"]
)

api_router.include_router(
    items.router,
    prefix="/items",
    tags=["Items"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)