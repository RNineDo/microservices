# infrastructure/db/repositories.py
import json
import os

class JsonProductRepository:
    """Dépôt gérant les accès disque au fichier JSON"""
    def __init__(self, file_path):
        self.file_path = file_path

    def add(self, product):
        data = []
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                try: data = json.load(f)
                except: data = []
        
        from .models import ProductDBModel
        data.append(ProductDBModel.to_dict(product))
        
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)