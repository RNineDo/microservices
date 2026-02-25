from pydantic import BaseModel
from typing import Optional


class NewPricingInput(BaseModel):
    product_id: str
    price: float = 0.0


class ModifyPricingInput(BaseModel):
    price: float


class PricingOutput(BaseModel):
    id: str
    product_id: str
    price: float
