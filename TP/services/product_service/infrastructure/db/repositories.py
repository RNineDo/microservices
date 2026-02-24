# infrastructure/db/repositories.py
import json
import os

class JsonImageRepository:
    """Gestion de l'accès aux données JSON"""
    def __init__(self, file_path):
        self.file_path = file_path

    def add(self, image):
        # Logique de bas niveau pour le JSON
        data = []
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                data = json.load(f)
        
        from .models import ImageDBModel
        data.append(ImageDBModel.to_json(image))
        
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)