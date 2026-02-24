# domain/models.py
from dataclasses import dataclass

@dataclass
class Product:
    """Entité métier du produit"""
    serial_number: str  # Le 'pk' du tableau
    nom: str
    description: str