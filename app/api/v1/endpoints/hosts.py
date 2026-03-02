from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.host import Host

router = APIRouter()

@router.get("/")
def get_hosts(db: Session = Depends(get_db)):
    return db.query(Host).all()