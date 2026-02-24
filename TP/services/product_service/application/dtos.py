# application/dtos.py
from dataclasses import dataclass

@dataclass
class ProductDTO:
    """Objet de transfert pour la création/modification"""
    serial_number: str
    nom: str
    description: str

