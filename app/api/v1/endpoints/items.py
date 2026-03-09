from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
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

    page: int = Query(1, ge=1),
    page_size: int = Query(500, ge=1, le=5000),

    sort: str = Query("asc", pattern="^(asc|desc)$"),

    db: Session = Depends(get_db)
):

    # Cek item ada atau tidak
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if start_date >= end_date:
        raise HTTPException(status_code=400, detail="Invalid date range")

    # Hitung offset
    offset = (page - 1) * page_size

    # Tentukan sorting
    order_by_clause = asc(ItemHistory.clock) if sort == "asc" else desc(ItemHistory.clock)

    # Query dengan pagination
    history = (
        db.query(
            ItemHistory.clock,
            ItemHistory.value_numeric
        )
        .filter(
            ItemHistory.item_id == item_id,
            ItemHistory.clock >= start_date,
            ItemHistory.clock <= end_date
        )
        .order_by(order_by_clause)
        .offset(offset)
        .limit(page_size)
        .all()
    )

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