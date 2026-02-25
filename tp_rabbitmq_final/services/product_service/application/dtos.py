from pydantic import BaseModel
from typing import Optional


class NewProductInput(BaseModel):
    name: str
    description: Optional[str] = None
    category: str = "other"


class ModifyProductInput(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None


class ProductOutput(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: str
    price: Optional[float] = None
    stock: Optional[int] = None
