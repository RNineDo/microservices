import uuid
from services.product_service.infrastructure.db.schema import ProductModel
from services.product_service.infrastructure.db.unit_of_work import ProductWorkUnit


class ProductStore:
    def __init__(self, uow: ProductWorkUnit):
        self._uow = uow

    def insert(self, data: dict) -> dict:
        with self._uow.begin() as session:
            record = ProductModel(
                id=str(uuid.uuid4()),
                name=data["name"],
                description=data.get("description"),
                category=data.get("category", "other"),
            )
            session.add(record)
            session.flush()
            return self._to_dict(record)

    def find_by_id(self, record_id: str) -> dict | None:
        with self._uow.begin() as session:
            record = session.query(ProductModel).filter_by(id=record_id).first()
            return self._to_dict(record) if record else None

    def list_all(self) -> list[dict]:
        with self._uow.begin() as session:
            records = session.query(ProductModel).all()
            return [self._to_dict(r) for r in records]

    def edit(self, record_id: str, data: dict) -> dict | None:
        with self._uow.begin() as session:
            record = session.query(ProductModel).filter_by(id=record_id).first()
            if not record:
                return None
            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            session.flush()
            return self._to_dict(record)

    def remove(self, record_id: str) -> bool:
        with self._uow.begin() as session:
            record = session.query(ProductModel).filter_by(id=record_id).first()
            if not record:
                return False
            session.delete(record)
            return True

    @staticmethod
    def _to_dict(record: ProductModel) -> dict:
        return {
            "id": record.id,
            "name": record.name,
            "description": record.description,
            "category": record.category,
        }
