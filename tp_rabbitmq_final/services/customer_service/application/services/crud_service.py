from services.customer_service.infrastructure.db.repository import ClientDataAccess
from services.customer_service.infrastructure.db.unit_of_work import ClientWorkUnit
from services.customer_service.application.dtos import NewClientInput, ModifyClientInput
from services.customer_service.infrastructure.messaging.pub_customer import CustomerEventEmitter


class ClientManager:
    def __init__(self, db_url: str, pub_addr: str = "tcp://*:5556"):
        self._uow = ClientWorkUnit(db_url)
        self._store = ClientDataAccess(self._uow)
        self._event_emitter = CustomerEventEmitter(pub_addr)

    def register(self, data: dict) -> dict:
        dto = NewClientInput(**data)
        record = self._store.insert(dto.model_dump())
        self._event_emitter.emit_created({
            "id": record["id"],
            "first_name": record["first_name"],
            "last_name": record["last_name"],
            "email": record["email"],
        })
        return record

    def fetch_one(self, client_id: str) -> dict:
        record = self._store.find_by_id(client_id)
        if not record:
            return {"error": "Client introuvable"}
        return record

    def fetch_all(self) -> dict:
        records = self._store.list_all()
        return {"items": records}

    def modify(self, data: dict) -> dict:
        client_id = data.pop("id")
        dto = ModifyClientInput(**data)
        updated = self._store.edit(client_id, dto.model_dump(exclude_none=True))
        if not updated:
            return {"error": "Client introuvable"}
        return updated

    def discard(self, client_id: str) -> dict:
        ok = self._store.remove(client_id)
        if not ok:
            return {"error": "Client introuvable"}
        return {"status": "supprime"}
