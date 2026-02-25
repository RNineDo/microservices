from pydantic import BaseModel
from typing import Optional, List


class NewOrderLineInput(BaseModel):
    product_id: str
    quantity: int = 1
    warehouse_id: Optional[str] = None


class NewOrderInput(BaseModel):
    customer_id: str
    lines: List[NewOrderLineInput] = []


class ModifyOrderInput(BaseModel):
    status: str


class OrderLineOutput(BaseModel):
    id: str
    order_id: str
    product_id: str
    quantity: int
    warehouse_id: Optional[str] = None


class OrderOutput(BaseModel):
    id: str
    customer_id: str
    status: str
    lines: List[OrderLineOutput] = []
