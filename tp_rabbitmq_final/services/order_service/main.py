import os
import time
from services.order_service.application.services.crud_service import PurchaseHandler
from services.order_service.infrastructure.messaging.rep_gateway import GatewayResponder


def main():
    db_url = os.getenv("DB_URL", "postgresql://admin:secret@postgres:5432/order_db")

    time.sleep(2)

    handler = PurchaseHandler(db_url)

    def dispatch(action: str, data: dict) -> dict:
        actions_map = {
            "create": lambda d: handler.register(d),
            "get": lambda d: handler.fetch_one(d["id"]),
            "update_status": lambda d: handler.modify_status(d),
        }
        fn = actions_map.get(action)
        if not fn:
            return {"error": f"Action inconnue: {action}"}
        return fn(data)

    responder = GatewayResponder(dispatch)
    responder.start_listening()


if __name__ == "__main__":
    main()
