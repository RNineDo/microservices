# infrastructure/db/models.py
class ProductPersistenceModel:
    """Traduit l'entité Domaine pour le stockage JSON"""
    @staticmethod
    def to_json(product):
        return {
            "pk": product.serial_number,
            "name": product.nom,
            "description": product.description
        }