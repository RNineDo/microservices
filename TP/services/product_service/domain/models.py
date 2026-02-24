# domain/models.py
from dataclasses import dataclass

@dataclass
class Product:
    """Entité Produit du domaine métier"""
    SerialNumber: str
    Nom: str
    Description: str