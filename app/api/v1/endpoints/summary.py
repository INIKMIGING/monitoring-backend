from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.api.deps import get_db
from sqlalchemy import text

router = APIRouter()

@router.get("/report")
def get_summary(
    range: str = Query(None, description="today | 7d"),
    start: datetime = Query(None),
    end: datetime = Query(None),
    db: Session = Depends(get_db)
):
    # --- 1. HANDLE DATE RANGE ---
    now = datetime.utcnow()

    if range == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif range == "7d":
        start = now - timedelta(days=7)
        end = now
    elif start and end:
        if (end - start).days > 60:
            raise HTTPException(status_code=400, detail="Max range is 60 days")
    else:
        raise HTTPException(
            status_code=400, 
            detail="Invalid parameter. Please provide 'range=today', 'range=7d', or 'start' & 'end' dates."
        )

    # --- 2. EXECUTE QUERY ---
    # Memastikan i.key_ digunakan di SELECT dan GROUP BY agar tidak terjadi 1054 error
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

    try:
        rows = db.execute(query, {"start": start, "end": end}).fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    # --- 3. MAPPING & GROUPING ---
    result = {
        "cpu": [],
        "memory": [],
        "bandwidth": [],
        "temperature": []
    }

    for row in rows:
        device = row.device
        key = row.item_key.lower()

        # Helper untuk memastikan angka rapi (2 desimal) dan tidak null
        def format_val(val):
            return round(float(val), 2) if val is not None else 0.0

        data = {
            "device": device,
            "min": format_val(row.min_value),
            "max": format_val(row.max_value),
            "avg": format_val(row.avg_value),
        }

        # Logika filter berdasarkan string di item_key
        if "cpu" in key:
            result["cpu"].append(data)
        elif "mem" in key:
            result["memory"].append(data)
        elif "net" in key or "bandwidth" in key:
            result["bandwidth"].append(data)
        elif "temp" in key:
            result["temperature"].append(data)

    # --- 4. DATA AVAILABILITY CHECK ---
    # Mengecek apakah semua list di dalam result kosong
    is_empty = all(len(result[k]) == 0 for k in result)

    # --- 5. FINAL RESPONSE STRUCTURE ---
    return {
        "status": "success",
        "message": "No data found for this period" if is_empty else "Data retrieved successfully",
        "total_categories": len(result),
        "is_data_available": not is_empty,
        "data": result
    }