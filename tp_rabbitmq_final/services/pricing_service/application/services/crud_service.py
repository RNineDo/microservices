from services.pricing_service.infrastructure.db.repository import PriceStore
from services.pricing_service.infrastructure.db.unit_of_work import PriceWorkUnit
from services.pricing_service.application.dtos import NewPricingInput, ModifyPricingInput


class PriceManager:
    def __init__(self, db_url: str):
        self._uow = PriceWorkUnit(db_url)
        self._store = PriceStore(self._uow)

    def register(self, data: dict) -> dict:
        dto = NewPricingInput(**data)
        return self._store.insert(dto.model_dump())

    def fetch_by_product(self, product_id: str) -> dict:
        record = self._store.find_by_product_id(product_id)
        if not record:
            return {"error": "Tarif introuvable pour ce produit"}
        return record

    def modify_by_product(self, data: dict) -> dict:
        product_id = data["product_id"]
        dto = ModifyPricingInput(amount=data.get("amount"), currency=data.get("currency"))
        updated = self._store.edit_by_product(product_id, dto.model_dump(exclude_none=True))
        if not updated:
            return {"error": "Tarif introuvable pour ce produit"}
        return updated

    def discard(self, pricing_id: str) -> dict:
        ok = self._store.remove(pricing_id)
        if not ok:
            return {"error": "Tarif introuvable"}
        return {"status": "supprime"}

    def auto_create_pricing(self, product_id: str):
        existing = self._store.find_by_product_id(product_id)
        if not existing:
            self._store.insert({"product_id": product_id, "amount": 0.0, "currency": "EUR"})
