# application/services.py
from .dtos import ImageDTO
from domain.models import Image
import uuid
from datetime import datetime

class ImageService:
    """Service applicatif pilotant le Unit of Work"""
    def __init__(self, uow):
        self.uow = uow

    def process_image_result(self, dto: ImageDTO):
        # On utilise le Unit of Work pour garantir l'intégrité
        with self.uow:
            new_image = Image(
                id=str(uuid.uuid4()),
                path=dto.path,
                status=dto.status,
                created_at=datetime.now()
            )
            self.uow.images.add(new_image)
            self.uow.commit()
        return new_image