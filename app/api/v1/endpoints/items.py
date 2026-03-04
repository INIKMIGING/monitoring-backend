from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.api.deps import get_db
from app.models.item import Item
from app.models.item_history import ItemHistory
from app.models.last_value import LastValue
from app.schemas.item import ItemHistoryResponse, LastValueResponse

router = APIRouter()

@router.get("/host/{host_id}")
def get_items_by_host(host_id: int, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.host_id == host_id).all()


@router.get(
    "/{item_id}/history",
    response_model=list[ItemHistoryResponse]
)
def get_item_history(
    item_id: int,
    start_date: datetime = Query(..., description="Start datetime (ISO 8601)"),
    end_date: datetime = Query(..., description="End datetime (ISO 8601)"),
    db: Session = Depends(get_db)
):

    # Cek item ada atau tidak
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Validasi range
    if start_date >= end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date must be earlier than end_date"
        )

    # Batasi range maksimal (anti abuse)
    max_range_days = 7
    if (end_date - start_date).days > max_range_days:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum allowed range is {max_range_days} days"
        )

    # Query
    history = (
        db.query(ItemHistory)
        .filter(
            ItemHistory.item_id == item_id,
            ItemHistory.clock >= start_date,
            ItemHistory.clock <= end_date
        )
        .order_by(ItemHistory.clock.asc())
        .limit(10000)
        .all()
    )

    # Return explicit schema
    return [
        ItemHistoryResponse(
            clock=h.clock,
            value_numeric=h.value_numeric
        )
        for h in history
    ]


@router.get(
    "/{item_id}/last",
    response_model=LastValueResponse
)
def get_last_value(item_id: int, db: Session = Depends(get_db)):

    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    last = db.query(LastValue).filter(
        LastValue.item_id == item_id
    ).first()

    if not last:
        raise HTTPException(status_code=404, detail="Last value not found")

    return LastValueResponse(
        last_clock=last.last_clock,
        last_value_numeric=last.last_value_numeric
    )