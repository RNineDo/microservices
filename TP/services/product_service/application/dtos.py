# application/dtos.py
from dataclasses import dataclass

@dataclass
class ImageDTO:
    """Objet de transfert de données"""
    path: str
    status: str