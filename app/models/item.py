from sqlalchemy import Column, BigInteger, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func

class Item(Base):
    __tablename__ = "items"

    id = Column(BigInteger, primary_key=True, index=True)
    itemid = Column(BigInteger, unique=True, nullable=False)
    host_id = Column(BigInteger, ForeignKey("hosts.id"), nullable=False)

    name = Column(String(255), nullable=False)
    key_ = Column(String(255))
    value_type = Column(String(32))
    units = Column(String(32))
    created_at = Column(TIMESTAMP, server_default=func.now())

    host = relationship("Host", back_populates="items")
    history = relationship("ItemHistory", back_populates="item")