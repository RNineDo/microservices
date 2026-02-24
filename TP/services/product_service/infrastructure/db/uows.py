# infrastructure/db/uows.py
from .repositories import JsonImageRepository

class JsonUnitOfWork:
    """Gestionnaire de contexte pour la transaction"""
    def __init__(self, file_path="database.json"):
        self.file_path = file_path

    def __enter__(self):
        self.images = JsonImageRepository(self.file_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ici on pourrait gérer le rollback si c'était du SQL
        pass

    def commit(self):
        # Pour du JSON, le commit est souvent implicite dans le repo, 
        # mais on respecte le pattern
        print("Transaction validée dans le JSON.")