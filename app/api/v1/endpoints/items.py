from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.api.deps import get_db
from app.models.item import Item
from app.models.item_history import ItemHistory
from app.models.last_value import LastValue

router = APIRouter()

@router.get("/host/{host_id}")
def get_items_by_host(host_id: int, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.host_id == host_id).all()


@router.get("/{item_id}/history")
def get_item_history(
    item_id: int,
    hours: int = Query(1, description="Last N hours"),
    db: Session = Depends(get_db)
):
    since = datetime.utcnow() - timedelta(hours=hours)

    return (
        db.query(ItemHistory)
        .filter(
            ItemHistory.item_id == item_id,
            ItemHistory.clock >= since
        )
        .order_by(ItemHistory.clock.asc())
        .all()
    )


@router.get("/{item_id}/last")
def get_last_value(item_id: int, db: Session = Depends(get_db)):
    return db.query(LastValue).filter(
        LastValue.item_id == item_id
    ).first()