import uuid
from services.order_service.infrastructure.db.schema import OrderModel, OrderLineModel
from services.order_service.infrastructure.db.unit_of_work import PurchaseWorkUnit


class PurchaseStore:
    def __init__(self, uow: PurchaseWorkUnit):
        self._uow = uow

    def insert(self, data: dict) -> dict:
        with self._uow.begin() as session:
            record = OrderModel(
                id=str(uuid.uuid4()),
                customer_id=data["customer_id"],
                status=data.get("status", "pending"),
            )
            session.add(record)
            session.flush()
            return self._to_dict(record)

    def find_by_id(self, record_id: str) -> dict | None:
        with self._uow.begin() as session:
            record = session.query(OrderModel).filter_by(id=record_id).first()
            return self._to_dict(record) if record else None

    def edit(self, record_id: str, data: dict) -> dict | None:
        with self._uow.begin() as session:
            record = session.query(OrderModel).filter_by(id=record_id).first()
            if not record:
                return None
            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            session.flush()
            return self._to_dict(record)

    @staticmethod
    def _to_dict(record: OrderModel) -> dict:
        return {
            "id": record.id,
            "customer_id": record.customer_id,
            "status": record.status,
        }


class PurchaseLineStore:
    def __init__(self, uow: PurchaseWorkUnit):
        self._uow = uow

    def insert(self, data: dict) -> dict:
        with self._uow.begin() as session:
            record = OrderLineModel(
                id=str(uuid.uuid4()),
                order_id=data["order_id"],
                product_id=data["product_id"],
                quantity=data.get("quantity", 1),
                warehouse_id=data.get("warehouse_id"),
            )
            session.add(record)
            session.flush()
            return self._to_dict(record)

    def find_by_order(self, order_id: str) -> list[dict]:
        with self._uow.begin() as session:
            records = session.query(OrderLineModel).filter_by(order_id=order_id).all()
            return [self._to_dict(r) for r in records]

    @staticmethod
    def _to_dict(record: OrderLineModel) -> dict:
        return {
            "id": record.id,
            "order_id": record.order_id,
            "product_id": record.product_id,
            "quantity": record.quantity,
            "warehouse_id": record.warehouse_id,
        }
