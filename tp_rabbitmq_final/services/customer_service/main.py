import os
from services.customer_service.application.services.crud_service import ClientManager
from services.customer_service.infrastructure.messaging.rep_gateway import GatewayResponder


def main():
    db_url = os.getenv("DB_URL", "postgresql://admin:secret@postgres:5432/customer_db")
    rmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

    manager = ClientManager(db_url)

    def dispatch(action: str, data: dict) -> dict:
        actions_map = {
            "create": lambda d: manager.register(d),
            "get": lambda d: manager.fetch_one(d["id"]),
            "get_all": lambda d: manager.fetch_all(),
            "update": lambda d: manager.modify(d),
            "delete": lambda d: manager.discard(d["id"]),
        }
        fn = actions_map.get(action)
        if not fn:
            return {"error": f"Action inconnue: {action}"}
        return fn(data)

    responder = GatewayResponder(dispatch, rmq_host)
    responder.start_listening()


if __name__ == "__main__":
    main()
