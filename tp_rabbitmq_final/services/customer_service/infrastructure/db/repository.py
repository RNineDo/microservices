import uuid
from services.customer_service.infrastructure.db.schema import CustomerModel
from services.customer_service.infrastructure.db.unit_of_work import ClientWorkUnit


class ClientDataAccess:
    def __init__(self, uow: ClientWorkUnit):
        self._uow = uow

    def insert(self, data: dict) -> dict:
        with self._uow.begin() as session:
            record = CustomerModel(
                id=str(uuid.uuid4()),
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                phone=data.get("phone"),
            )
            session.add(record)
            session.flush()
            return self._to_dict(record)

    def find_by_id(self, record_id: str) -> dict | None:
        with self._uow.begin() as session:
            record = session.query(CustomerModel).filter_by(id=record_id).first()
            return self._to_dict(record) if record else None

    def list_all(self) -> list[dict]:
        with self._uow.begin() as session:
            records = session.query(CustomerModel).all()
            return [self._to_dict(r) for r in records]

    def edit(self, record_id: str, data: dict) -> dict | None:
        with self._uow.begin() as session:
            record = session.query(CustomerModel).filter_by(id=record_id).first()
            if not record:
                return None
            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            session.flush()
            return self._to_dict(record)

    def remove(self, record_id: str) -> bool:
        with self._uow.begin() as session:
            record = session.query(CustomerModel).filter_by(id=record_id).first()
            if not record:
                return False
            session.delete(record)
            return True

    @staticmethod
    def _to_dict(record: CustomerModel) -> dict:
        return {
            "id": record.id,
            "first_name": record.first_name,
            "last_name": record.last_name,
            "email": record.email,
            "phone": record.phone,
        }
