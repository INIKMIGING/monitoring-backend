from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, Float, Index, desc
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ItemHistory(Base):
    __tablename__ = "item_history"

    id = Column(BigInteger, primary_key=True)
    item_id = Column(BigInteger, ForeignKey("items.id"), nullable=False)
    clock = Column(DateTime, nullable=False, index=True)
    value_numeric = Column(Float, nullable=False)

    item = relationship("Item", back_populates="history")

    __table_args__ = (
        Index("idx_item_clock", "item_id", "clock"),
        Index("idx_item_clock_desc", "item_id", desc("clock")),
        Index("idx_clock", "clock"), 
    )