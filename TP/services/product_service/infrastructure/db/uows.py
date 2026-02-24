# infrastructure/db/uows.py (Unit of Work)
class JsonUnitOfWork:
    """Assure l'intégrité de l'opération (Pattern UoW)"""
    def __init__(self, file_path="products_db.json"):
        self.file_path = file_path

    def __enter__(self):
        from .repositories import JsonProductRepository
        self.products = JsonProductRepository(self.file_path)
        return self

    def __exit__(self, *args):
        pass

    def commit(self):
        print(f"Produit sauvegardé avec succès dans {self.file_path}.")