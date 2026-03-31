from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password


def seed_admin():
    db: Session = SessionLocal()

    admin = db.query(User).filter(User.username == "admin").first()

    if not admin:
        admin = User(
            username="admin",
            password_hash=hash_password("admin123")
        )

        db.add(admin)
        db.commit()
        print("✅ Admin user created")

    else:
        print("⚠️ Admin already exists")

    db.close()


if __name__ == "__main__":
    seed_admin()