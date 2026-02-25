from enum import StrEnum
from pydantic import BaseModel
from typing import Optional


class ProductCategory(StrEnum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"
    OTHER = "other"


class ProductItem(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    category: ProductCategory = ProductCategory.OTHER
