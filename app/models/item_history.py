from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, Float, Index
from sqlalchemy.orm import relationship
from app.db.base import Base

class ItemHistory(Base):
    __tablename__ = "item_history"

    id = Column(BigInteger, primary_key=True)
    item_id = Column(BigInteger, ForeignKey("items.id"), nullable=False)
    clock = Column(DateTime, nullable=False)
    value_numeric = Column(Float, nullable=False)

    item = relationship("Item", back_populates="history")

    __table_args__ = (
        Index("idx_item_clock", "item_id", "clock"),
    )