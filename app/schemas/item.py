from pydantic import BaseModel
from datetime import datetime


class ItemHistoryResponse(BaseModel):
    clock: datetime
    value_numeric: float

    class Config:
        from_attributes = True


class LastValueResponse(BaseModel):
    last_clock: datetime
    last_value_numeric: float

    class Config:
        from_attributes = True