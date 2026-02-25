from pydantic import BaseModel
from typing import Optional


class StorageLocation(BaseModel):
    id: Optional[str] = None
    name: str
    address: Optional[str] = None


class StockEntry(BaseModel):
    id: Optional[str] = None
    product_id: str
    warehouse_id: str
    quantity: int = 0
