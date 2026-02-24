# infrastructure/db/models.py
class ImageDBModel:
    """Représentation de l'image telle qu'elle est stockée en JSON"""
    @staticmethod
    def to_json(entity):
        return {
            "id": entity.id,
            "path": entity.path,
            "status": entity.status,
            "created_at": entity.created_at.isoformat()
        }