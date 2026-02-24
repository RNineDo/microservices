# application/dtos.py
from dataclasses import dataclass

@dataclass
class ProductDTO:
    """Objet utilisé pour transférer les données vers le service"""
    SerialNumber: str
    Nom: str
    Description: str