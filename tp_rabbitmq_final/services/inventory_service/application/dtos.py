from pydantic import BaseModel
from typing import Optional


class NewWarehouseInput(BaseModel):
    name: str
    address: Optional[str] = None


class WarehouseOutput(BaseModel):
    id: str
    name: str
    address: Optional[str] = None


class NewStockInput(BaseModel):
    product_id: str
    warehouse_id: str
    quantity: int = 0


class ModifyStockInput(BaseModel):
    quantity: int


class StockOutput(BaseModel):
    id: str
    product_id: str
    warehouse_id: str
    quantity: int
