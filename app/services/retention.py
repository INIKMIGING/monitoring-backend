from datetime import datetime, timedelta
from app.db.session import SessionLocal
from app.models.item_history import ItemHistory

BATCH_SIZE = 1000

def delete_old_data():
    db = SessionLocal()

    try:
        cutoff = datetime.utcnow() - timedelta(days=30)

        while True:
            # ambil id dulu
            ids = (
                db.query(ItemHistory.id)
                .filter(ItemHistory.clock < cutoff)
                .limit(BATCH_SIZE)
                .all()
            )

            if not ids:
                break

            id_list = [i[0] for i in ids]

            db.query(ItemHistory).filter(
                ItemHistory.id.in_(id_list)
            ).delete(synchronize_session=False)

            db.commit()

        print("[Retention] Cleanup done (batched)")

    except Exception as e:
        db.rollback()
        print(f"[Retention] Error: {e}")

    finally:
        db.close()