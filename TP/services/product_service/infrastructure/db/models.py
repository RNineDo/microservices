# infrastructure/db/models.py
class ProductDBModel:
    """Deuxième modèle : gère la sérialisation JSON"""
    @staticmethod
    def to_dict(product):
        return {
            "serial_number": product.SerialNumber,
            "nom": product.Nom,
            "description": product.Description
        }
