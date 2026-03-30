from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import SessionLocal
from app.models.item_history import ItemHistory

router = APIRouter(prefix="/metrics", tags=["metrics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{item_id}/chart")
def get_chart_data(
    item_id: int,
    range: str = Query("1h"),
    db: Session = Depends(get_db)
):

    now = datetime.utcnow()

    if range == "1h":
        start = now - timedelta(hours=1)

    elif range == "6h":
        start = now - timedelta(hours=6)

    elif range == "24h":
        start = now - timedelta(hours=24)

    elif range == "7d":
        start = now - timedelta(days=7)

    else:
        start = now - timedelta(hours=1)

    rows = (
        db.query(ItemHistory.clock, ItemHistory.value)
        .filter(
            ItemHistory.item_id == item_id,
            ItemHistory.clock >= start
        )
        .order_by(ItemHistory.clock.asc())
        .limit(2000)
        .all()
    )

    return {
        "item_id": item_id,
        "points": [
            {"ts": r.clock, "value": r.value}
            for r in rows
        ]
    }

@router.get("/{item_id}/last")
def get_last(item_id: int, db: Session = Depends(get_db)):

    row = (
        db.query(ItemHistory)
        .filter(ItemHistory.item_id == item_id)
        .order_by(ItemHistory.clock.desc())
        .first()
    )

    return row