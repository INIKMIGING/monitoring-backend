from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.host import Host

router = APIRouter()

@router.get("/")
def get_hosts(db: Session = Depends(get_db)):
    return db.query(Host).all()

@router.put("/{host_id}/location")
def update_location(host_id: int, location: str, db: Session = Depends(get_db)):
    host = db.query(Host).filter(Host.id == host_id).first()

    if not host:
        return {"error": "Host not found"}

    host.location = location
    db.commit()
    db.refresh(host)

    return {
        "message": "Location updated",
        "data": host
    }
