import uuid
from services.pricing_service.infrastructure.db.schema import PricingModel
from services.pricing_service.infrastructure.db.unit_of_work import PriceWorkUnit


class PriceStore:
    def __init__(self, uow: PriceWorkUnit):
        self._uow = uow

    def insert(self, data: dict) -> dict:
        with self._uow.begin() as session:
            record = PricingModel(
                id=str(uuid.uuid4()),
                product_id=data["product_id"],
                amount=data.get("amount", 0.0),
                currency=data.get("currency", "EUR"),
            )
            session.add(record)
            session.flush()
            return self._to_dict(record)

    def find_by_product_id(self, product_id: str) -> dict | None:
        with self._uow.begin() as session:
            record = session.query(PricingModel).filter_by(product_id=product_id).first()
            return self._to_dict(record) if record else None

    def edit_by_product(self, product_id: str, data: dict) -> dict | None:
        with self._uow.begin() as session:
            record = session.query(PricingModel).filter_by(product_id=product_id).first()
            if not record:
                return None
            for key, value in data.items():
                if hasattr(record, key) and value is not None:
                    setattr(record, key, value)
            session.flush()
            return self._to_dict(record)

    def remove(self, record_id: str) -> bool:
        with self._uow.begin() as session:
            record = session.query(PricingModel).filter_by(id=record_id).first()
            if not record:
                return False
            session.delete(record)
            return True

    @staticmethod
    def _to_dict(record: PricingModel) -> dict:
        return {
            "id": record.id,
            "product_id": record.product_id,
            "amount": record.amount,
            "currency": record.currency,
        }
