from pydantic import BaseModel
from typing import Optional


class ClientProfile(BaseModel):
    id: Optional[str] = None
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
