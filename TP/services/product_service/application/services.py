# application/services.py
from domain.models import Product

class ProductService:
    """Service applicatif piloté par le Unit of Work"""
    def __init__(self, uow):
        self.uow = uow

    def create_product(self, dto: ProductDTO):
        with self.uow:
            product = Product(
                serial_number=dto.serial_number,
                nom=dto.nom,
                description=dto.description
            )
            self.uow.products.add(product)
            self.uow.commit()
        return product