# infrastructure/db/uows.py
from .repositories import JsonProductRepository

class JsonUnitOfWork:
    """Gestionnaire de transaction (Pattern Unit of Work)"""
    def __init__(self, file_path="products.json"):
        self.file_path = file_path

    def __enter__(self):
        self.products = JsonProductRepository(self.file_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass # Gestion du rollback si nécessaire

    def commit(self):
        print("Commit : Données persistées en JSON.")