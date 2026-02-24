# application/services.py
class ProductService:
    """Service orchestrant les opérations sur les produits"""
    def __init__(self, uow):
        self.uow = uow

    def add_product(self, dto: ProductDTO):
        with self.uow:
            from domain.models import Product
            # Transformation du DTO en Entité Métier
            product = Product(
                SerialNumber=dto.SerialNumber,
                Nom=dto.Nom,
                Description=dto.Description
            )
            self.uow.products.add(product)
            self.uow.commit()
        return product