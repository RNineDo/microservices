import os
import time
import threading
from services.inventory_service.application.services.crud_service import StockController
from services.inventory_service.infrastructure.messaging.rep_gateway import GatewayResponder
from services.inventory_service.infrastructure.messaging.sub_product_created import ProductCreatedListener
from services.inventory_service.infrastructure.messaging.sub_orderline_created import OrderLineCreatedListener
from services.inventory_service.infrastructure.messaging.pair_product import ProductPairServer


def main():
    db_url = os.getenv("DB_URL", "postgresql://admin:secret@postgres:5432/inventory_db")

    time.sleep(2)

    controller = StockController(db_url)

    def dispatch(action: str, data: dict) -> dict:
        actions_map = {
            "create_warehouse": lambda d: controller.register_warehouse(d),
            "get_warehouse": lambda d: controller.fetch_warehouse(d["id"]),
            "get_all_warehouses": lambda d: controller.fetch_all_warehouses(),
            "create_inventory": lambda d: controller.register_stock(d),
            "get_inventory_by_product": lambda d: controller.fetch_stock_by_product(d["product_id"]),
            "update_inventory": lambda d: controller.modify_stock(d),
        }
        fn = actions_map.get(action)
        if not fn:
            return {"error": f"Action inconnue: {action}"}
        return fn(data)

    def on_product_created(event_data: dict):
        product_id = event_data.get("id")
        if product_id:
            controller.auto_create_stock(product_id)

    def on_orderline_created(event_data: dict):
        product_id = event_data.get("product_id")
        quantity = event_data.get("quantity", 1)
        warehouse_id = event_data.get("warehouse_id")
        if product_id:
            controller.decrement_stock(product_id, quantity, warehouse_id)

    def pair_handler(message: dict) -> dict:
        action = message.get("action")
        if action == "get_stock":
            product_id = message.get("product_id")
            return controller.fetch_stock_by_product(product_id)
        return {"error": "Action PAIR inconnue"}

    product_listener = ProductCreatedListener(on_product_created)
    orderline_listener = OrderLineCreatedListener(on_orderline_created)
    pair_server = ProductPairServer(pair_handler)

    threading.Thread(target=product_listener.start_listening, daemon=True).start()
    threading.Thread(target=orderline_listener.start_listening, daemon=True).start()
    threading.Thread(target=pair_server.start_listening, daemon=True).start()

    responder = GatewayResponder(dispatch)
    responder.start_listening()


if __name__ == "__main__":
    main()
