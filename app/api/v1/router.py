from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api.deps import get_db
from app.api.v1.endpoints import hosts, items

api_router = APIRouter()

@api_router.get("/monitoring_db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {
        "database": "connected",
        "result": result.scalar()
    }

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