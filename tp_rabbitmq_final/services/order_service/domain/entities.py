from enum import StrEnum
from pydantic import BaseModel
from typing import Optional, List


class PurchaseStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PurchaseLine(BaseModel):
    id: Optional[str] = None
    order_id: Optional[str] = None
    product_id: str
    quantity: int = 1
    warehouse_id: Optional[str] = None


class Purchase(BaseModel):
    id: Optional[str] = None
    customer_id: str
    status: PurchaseStatus = PurchaseStatus.PENDING
    lines: List[PurchaseLine] = []
