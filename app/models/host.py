from sqlalchemy import Column, BigInteger, String, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.sql import func

class Host(Base):
    __tablename__ = "hosts"

    id = Column(BigInteger, primary_key=True, index=True)
    hostid = Column(BigInteger, unique=True, nullable=False)
    host = Column(String(128), nullable=False)
    visible_name = Column(String(128))
    location = Column(String(128))
    created_at = Column(TIMESTAMP, server_default=func.now())

    items = relationship("Item", back_populates="host")