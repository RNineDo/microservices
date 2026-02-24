import zmq
import json
from application.services import ProductService
from application.dtos import ProductDTO
from infrastructure.db.uows import JsonUnitOfWork

def main():
    # 1. Initialisation des composants selon l'architecture
    uow = JsonUnitOfWork("products_db.json")
    service = ProductService(uow)

    # 2. Configuration du socket ZMQ (Modèle REQ/REP du schéma)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")  # Port d'écoute pour le FRONT

    print("--- PRODUCT SERVICE ACTIF ---")
    print("En attente de commandes du FRONT (REQ/REP)...")

    while True:
        try:
            # Réception du message (format attendu: JSON string)
            message = socket.recv_json()
            print(f"Requête reçue : {message}")

            # 3. Mapping vers le DTO et exécution du service
            dto = ProductDTO(
                serial_number=message.get("SerialNumber"),
                nom=message.get("Nom"),
                description=message.get("Description")
            )

            # Traitement par la couche application
            product = service.create_product(dto)

            # 4. Réponse au FRONT
            socket.send_json({
                "status": "success",
                "message": f"Produit {product.serial_number} enregistré."
            })

        except Exception as e:
            print(f"Erreur : {e}")
            socket.send_json({"status": "error", "message": str(e)})

if __name__ == "__main__":
    main()