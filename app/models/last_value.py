from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, Float
from app.db.base_class import Base

class LastValue(Base):
    __tablename__ = "last_values"

    item_id = Column(BigInteger, ForeignKey("items.id"), primary_key=True)
    last_clock = Column(DateTime, nullable=False)
    last_value_numeric = Column(Float, nullable=False)