from services.inventory_service.infrastructure.db.repository import WarehouseStore, StockStore
from services.inventory_service.infrastructure.db.unit_of_work import InventoryWorkUnit
from services.inventory_service.application.dtos import NewWarehouseInput, NewStockInput, ModifyStockInput


class StockController:
    def __init__(self, db_url: str):
        self._uow = InventoryWorkUnit(db_url)
        self._warehouse_store = WarehouseStore(self._uow)
        self._stock_store = StockStore(self._uow)

    def register_warehouse(self, data: dict) -> dict:
        dto = NewWarehouseInput(**data)
        return self._warehouse_store.insert(dto.model_dump())

    def fetch_warehouse(self, wh_id: str) -> dict:
        record = self._warehouse_store.find_by_id(wh_id)
        if not record:
            return {"error": "Entrepot introuvable"}
        return record

    def fetch_all_warehouses(self) -> dict:
        records = self._warehouse_store.list_all()
        return {"items": records}

    def register_stock(self, data: dict) -> dict:
        dto = NewStockInput(**data)
        return self._stock_store.insert(dto.model_dump())

    def fetch_stock_by_product(self, product_id: str) -> dict:
        records = self._stock_store.find_by_product(product_id)
        if not records:
            return {"error": "Aucun stock pour ce produit"}
        total = sum(r["quantity"] for r in records)
        return {"product_id": product_id, "entries": records, "quantity": total}

    def modify_stock(self, data: dict) -> dict:
        warehouse_id = data["warehouse_id"]
        product_id = data["product_id"]
        dto = ModifyStockInput(quantity=data["quantity"])
        updated = self._stock_store.edit_by_keys(warehouse_id, product_id, dto.model_dump())
        if not updated:
            return {"error": "Entree de stock introuvable"}
        return updated

    def auto_create_stock(self, product_id: str):
        warehouses = self._warehouse_store.list_all()
        for wh in warehouses:
            existing = self._stock_store.find_by_warehouse_product(wh["id"], product_id)
            if not existing:
                self._stock_store.insert({
                    "product_id": product_id,
                    "warehouse_id": wh["id"],
                    "quantity": 0,
                })

    def decrement_stock(self, product_id: str, quantity: int, warehouse_id: str = None):
        if warehouse_id:
            entry = self._stock_store.find_by_warehouse_product(warehouse_id, product_id)
            if entry:
                new_qty = max(0, entry["quantity"] - quantity)
                self._stock_store.edit_by_keys(warehouse_id, product_id, {"quantity": new_qty})
        else:
            entries = self._stock_store.find_by_product(product_id)
            remaining = quantity
            for entry in entries:
                if remaining <= 0:
                    break
                available = entry["quantity"]
                deducted = min(available, remaining)
                new_qty = available - deducted
                self._stock_store.edit_by_keys(entry["warehouse_id"], product_id, {"quantity": new_qty})
                remaining -= deducted
