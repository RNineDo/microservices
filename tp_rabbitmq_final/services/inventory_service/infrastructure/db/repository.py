import uuid
from services.inventory_service.infrastructure.db.schema import WarehouseModel, InventoryModel
from services.inventory_service.infrastructure.db.unit_of_work import InventoryWorkUnit


class WarehouseStore:
    def __init__(self, uow: InventoryWorkUnit):
        self._uow = uow

    def insert(self, data: dict) -> dict:
        with self._uow.begin() as session:
            record = WarehouseModel(
                id=str(uuid.uuid4()),
                name=data["name"],
                address=data.get("address"),
            )
            session.add(record)
            session.flush()
            return self._to_dict(record)

    def find_by_id(self, record_id: str) -> dict | None:
        with self._uow.begin() as session:
            record = session.query(WarehouseModel).filter_by(id=record_id).first()
            return self._to_dict(record) if record else None

    def list_all(self) -> list[dict]:
        with self._uow.begin() as session:
            records = session.query(WarehouseModel).all()
            return [self._to_dict(r) for r in records]

    @staticmethod
    def _to_dict(record: WarehouseModel) -> dict:
        return {
            "id": record.id,
            "name": record.name,
            "address": record.address,
        }


class StockStore:
    def __init__(self, uow: InventoryWorkUnit):
        self._uow = uow

    def insert(self, data: dict) -> dict:
        with self._uow.begin() as session:
            record = InventoryModel(
                id=str(uuid.uuid4()),
                product_id=data["product_id"],
                warehouse_id=data["warehouse_id"],
                quantity=data.get("quantity", 0),
            )
            session.add(record)
            session.flush()
            return self._to_dict(record)

    def find_by_product(self, product_id: str) -> list[dict]:
        with self._uow.begin() as session:
            records = session.query(InventoryModel).filter_by(product_id=product_id).all()
            return [self._to_dict(r) for r in records]

    def find_by_warehouse_product(self, warehouse_id: str, product_id: str) -> dict | None:
        with self._uow.begin() as session:
            record = session.query(InventoryModel).filter_by(
                warehouse_id=warehouse_id, product_id=product_id
            ).first()
            return self._to_dict(record) if record else None

    def edit_by_keys(self, warehouse_id: str, product_id: str, data: dict) -> dict | None:
        with self._uow.begin() as session:
            record = session.query(InventoryModel).filter_by(
                warehouse_id=warehouse_id, product_id=product_id
            ).first()
            if not record:
                return None
            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            session.flush()
            return self._to_dict(record)

    @staticmethod
    def _to_dict(record: InventoryModel) -> dict:
        return {
            "id": record.id,
            "product_id": record.product_id,
            "warehouse_id": record.warehouse_id,
            "quantity": record.quantity,
        }
