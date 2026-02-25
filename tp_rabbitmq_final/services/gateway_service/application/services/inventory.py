from services.gateway_service.infrastructure.messaging.req_inventory import InventoryRequester


class InventoryProxy:
    def __init__(self):
        self._requester = InventoryRequester()

    def register_warehouse(self, payload: dict) -> dict:
        return self._requester.send("create_warehouse", payload)

    def fetch_all_warehouses(self) -> dict:
        return self._requester.send("get_all_warehouses")

    def register_stock(self, payload: dict) -> dict:
        return self._requester.send("create_inventory", payload)

    def fetch_stock_by_product(self, product_pk: str) -> dict:
        return self._requester.send("get_inventory_by_product", {"product_id": product_pk})

    def modify_stock(self, warehouse_pk: str, product_pk: str, payload: dict) -> dict:
        payload["warehouse_id"] = warehouse_pk
        payload["product_id"] = product_pk
        return self._requester.send("update_inventory", payload)
