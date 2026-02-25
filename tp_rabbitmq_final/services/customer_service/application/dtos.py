from pydantic import BaseModel
from typing import Optional


class NewClientInput(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None


class ModifyClientInput(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class ClientOutput(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
