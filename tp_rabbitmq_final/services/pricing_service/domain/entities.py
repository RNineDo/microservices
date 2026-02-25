from pydantic import BaseModel
from typing import Optional


class PriceRecord(BaseModel):
    id: Optional[str] = None
    product_id: str
    amount: float = 0.0
    currency: str = "EUR"
