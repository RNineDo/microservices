import os
from services.product_service.application.services.crud_service import ProductHandler
from services.product_service.infrastructure.messaging.rep_gateway import GatewayResponder


def main():
    db_url = os.getenv("DB_URL", "postgresql://admin:secret@postgres:5432/product_db")
    rmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

    handler = ProductHandler(db_url, rmq_host)

    def dispatch(action: str, data: dict) -> dict:
        actions_map = {
            "create": lambda d: handler.register(d),
            "get": lambda d: handler.fetch_one(d["id"]),
            "get_all": lambda d: handler.fetch_all(),
            "update": lambda d: handler.modify(d),
            "delete": lambda d: handler.discard(d["id"]),
        }
        fn = actions_map.get(action)
        if not fn:
            return {"error": f"Action inconnue: {action}"}
        return fn(data)

    responder = GatewayResponder(dispatch, rmq_host)
    responder.start_listening()


if __name__ == "__main__":
    main()
