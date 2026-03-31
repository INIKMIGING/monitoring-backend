from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.api.deps import get_db
from sqlalchemy import text

router = APIRouter()

@router.get("/report")
def get_summary(
    range: str = Query(None),  # today | 7d
    start: datetime = None,
    end: datetime = None,
    db: Session = Depends(get_db)
):
    # --- HANDLE RANGE ---
    now = datetime.utcnow()

    if range == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now

    elif range == "7d":
        start = now - timedelta(days=7)
        end = now

    elif start and end:
        if (end - start).days > 60:
            return {"error": "Max range is 60 days"}

    else:
        return {"error": "Invalid parameter"}

    # --- QUERY ---
    query = text("""
        SELECT 
            h.host as device,
            i.key_ as item_key,
            MIN(ih.value_numeric) as min_value,
            MAX(ih.value_numeric) as max_value,
            AVG(ih.value_numeric) as avg_value
        FROM item_history ih
        JOIN items i ON ih.item_id = i.id
        JOIN hosts h ON i.host_id = h.id
        WHERE ih.clock BETWEEN :start AND :end
        GROUP BY h.host, i.key_
    """)

    rows = db.execute(query, {"start": start, "end": end}).fetchall()

    # --- GROUPING ---
    result = {
        "cpu": [],
        "memory": [],
        "bandwidth": []
    }

    for row in rows:
        device = row.device
        key = row.item_key.lower()

        data = {
            "device": device,
            "min": float(row.min_value) if row.min_value else None,
            "max": float(row.max_value) if row.max_value else None,
            "avg": float(row.avg_value) if row.avg_value else None,
        }

        # mapping type
        if "cpu" in key:
            result["cpu"].append(data)
        elif "mem" in key:
            result["memory"].append(data)
        elif "net" in key or "bandwidth" in key:
            result["bandwidth"].append(data)

    return result