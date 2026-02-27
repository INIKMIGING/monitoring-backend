from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base # Tambahkan declarative_base
from app.core.config import settings

# 1. Definisikan Base di sini
Base = declarative_base() 

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)