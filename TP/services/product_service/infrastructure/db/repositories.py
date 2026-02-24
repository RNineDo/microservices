# infrastructure/db/repositories.py
import json
import os

class JsonProductRepository:
    """Dépôt pour l'accès aux données (Pattern Repository)"""
    def __init__(self, file_path):
        self.file_path = file_path

    def add(self, product):
        from .models import ProductPersistenceModel
        data = self._read_all()
        data.append(ProductPersistenceModel.to_json(product))
        self._write_all(data)

    def _read_all(self):
        if not os.path.exists(self.file_path): return []
        with open(self.file_path, 'r') as f:
            try: return json.load(f)
            except: return []

    def _write_all(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)