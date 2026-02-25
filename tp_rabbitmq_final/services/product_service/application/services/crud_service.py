from services.product_service.infrastructure.db.repository import ProductStore
from services.product_service.infrastructure.db.unit_of_work import ProductWorkUnit
from services.product_service.application.dtos import NewProductInput, ModifyProductInput, ProductOutput
from services.product_service.infrastructure.messaging.pub_product import ProductEventEmitter
from services.product_service.infrastructure.messaging.pair_pricing import PricingPairClient
from services.product_service.infrastructure.messaging.pair_inventory import InventoryPairClient


class ProductHandler:
    def __init__(self, db_url: str, rabbitmq_host: str):
        self._uow = ProductWorkUnit(db_url)
        self._store = ProductStore(self._uow)
        self._event_emitter = ProductEventEmitter(rabbitmq_host)
        self._pricing_client = PricingPairClient(rabbitmq_host)
        self._inventory_client = InventoryPairClient(rabbitmq_host)

    def register(self, data: dict) -> dict:
        dto = NewProductInput(**data)
        record = self._store.insert(dto.model_dump())
        self._event_emitter.emit_created({
            "id": record["id"],
            "name": record["name"],
            "category": record["category"],
        })
        return record

    def fetch_one(self, product_id: str) -> dict:
        record = self._store.find_by_id(product_id)
        if not record:
            return {"error": "Produit introuvable"}
        pricing_info = self._pricing_client.fetch_price(product_id)
        inventory_info = self._inventory_client.fetch_stock(product_id)
        result = ProductOutput(
            id=record["id"],
            name=record["name"],
            description=record.get("description"),
            category=record["category"],
            price=pricing_info.get("price"),
            stock=inventory_info.get("quantity"),
        )
        return result.model_dump()

    def fetch_all(self) -> dict:
        records = self._store.list_all()
        return {"items": records}

    def modify(self, data: dict) -> dict:
        product_id = data.pop("id")
        dto = ModifyProductInput(**data)
        updated = self._store.edit(product_id, dto.model_dump(exclude_none=True))
        if not updated:
            return {"error": "Produit introuvable"}
        return updated

    def discard(self, product_id: str) -> dict:
        ok = self._store.remove(product_id)
        if not ok:
            return {"error": "Produit introuvable"}
        return {"status": "supprime"}
