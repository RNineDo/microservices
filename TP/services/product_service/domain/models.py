# domain/models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Image:
    """Entité métier pure"""
    id: str
    path: str
    status: str
    created_at: datetime