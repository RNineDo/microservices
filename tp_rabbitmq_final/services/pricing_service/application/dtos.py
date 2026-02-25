from pydantic import BaseModel
from typing import Optional


class NewPricingInput(BaseModel):
    product_id: str
    amount: float = 0.0
    currency: str = "EUR"


class ModifyPricingInput(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None


class PricingOutput(BaseModel):
    id: str
    product_id: str
    amount: float
    currency: str
