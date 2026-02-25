from services.order_service.infrastructure.db.repository import PurchaseStore, PurchaseLineStore
from services.order_service.infrastructure.db.unit_of_work import PurchaseWorkUnit
from services.order_service.application.dtos import NewOrderInput, ModifyOrderInput
from services.order_service.infrastructure.messaging.pub_order_created import OrderEventEmitter


class PurchaseHandler:
    def __init__(self, db_url: str, pub_addr: str = "tcp://*:5556"):
        self._uow = PurchaseWorkUnit(db_url)
        self._store = PurchaseStore(self._uow)
        self._line_store = PurchaseLineStore(self._uow)
        self._event_emitter = OrderEventEmitter(pub_addr)

    def register(self, data: dict) -> dict:
        dto = NewOrderInput(**data)
        order_record = self._store.insert({
            "customer_id": dto.customer_id,
            "status": "pending",
        })
        order_id = order_record["id"]
        created_lines = []
        for line in dto.lines:
            line_record = self._line_store.insert({
                "order_id": order_id,
                "product_id": line.product_id,
                "quantity": line.quantity,
                "warehouse_id": line.warehouse_id,
            })
            created_lines.append(line_record)
            self._event_emitter.emit_orderline_created({
                "id": line_record["id"],
                "order_id": order_id,
                "product_id": line.product_id,
                "quantity": line.quantity,
                "warehouse_id": line.warehouse_id,
            })
        self._event_emitter.emit_order_created({
            "id": order_id,
            "customer_id": dto.customer_id,
            "status": "pending",
        })
        order_record["lines"] = created_lines
        return order_record

    def fetch_one(self, order_id: str) -> dict:
        record = self._store.find_by_id(order_id)
        if not record:
            return {"error": "Commande introuvable"}
        lines = self._line_store.find_by_order(order_id)
        record["lines"] = lines
        return record

    def modify_status(self, data: dict) -> dict:
        order_id = data.get("id")
        dto = ModifyOrderInput(status=data.get("status", "pending"))
        updated = self._store.edit(order_id, {"status": dto.status})
        if not updated:
            return {"error": "Commande introuvable"}
        return updated
