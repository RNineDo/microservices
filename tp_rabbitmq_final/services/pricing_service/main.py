import os
import time
import threading
from services.pricing_service.application.services.crud_service import PriceManager
from services.pricing_service.infrastructure.messaging.rep_gateway import GatewayResponder
from services.pricing_service.infrastructure.messaging.sub_product_created import ProductCreatedListener
from services.pricing_service.infrastructure.messaging.pair_product import ProductPairServer


def main():
    db_url = os.getenv("DB_URL", "postgresql://admin:secret@postgres:5432/pricing_db")

    time.sleep(2)

    manager = PriceManager(db_url)

    def dispatch(action: str, data: dict) -> dict:
        actions_map = {
            "create": lambda d: manager.register(d),
            "get_by_product": lambda d: manager.fetch_by_product(d["product_id"]),
            "update_by_product": lambda d: manager.modify_by_product(d),
            "delete": lambda d: manager.discard(d["id"]),
        }
        fn = actions_map.get(action)
        if not fn:
            return {"error": f"Action inconnue: {action}"}
        return fn(data)

    def on_product_created(event_data: dict):
        product_id = event_data.get("id")
        if product_id:
            manager.auto_create_pricing(product_id)

    def pair_handler(message: dict) -> dict:
        action = message.get("action")
        if action == "get_price":
            product_id = message.get("product_id")
            return manager.fetch_by_product(product_id)
        return {"error": "Action PAIR inconnue"}

    product_listener = ProductCreatedListener(on_product_created)
    pair_server = ProductPairServer(pair_handler)

    threading.Thread(target=product_listener.start_listening, daemon=True).start()
    threading.Thread(target=pair_server.start_listening, daemon=True).start()

    responder = GatewayResponder(dispatch)
    responder.start_listening()


if __name__ == "__main__":
    main()
